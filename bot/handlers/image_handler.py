"""Image handler for photo processing and style selection."""
import logging
from datetime import datetime, timezone
from bson import ObjectId
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.db.repositories import UserRepository, ProcessImgRepository, BotJobsPhotoRepository, BotJobsVideoRepository, NodeRepository
from bot.db.models import ProcessImg, BotJobsPhoto, BotJobsVideo
from bot.languages import get_text
from bot.keyboards import kb_image_actions, kb_style_selection, kb_face_swap_options, kb_photo_swap_options, kb_video_swap_options, kb_dynamic_style_selection
from bot.texts import IMAGE_ACTION_PROMPT, STYLE_SELECTION_PROMPT
from bot.callbacks import (
    IMAGE_GENERATE, IMAGE_FACE_SWAP, IMAGE_VIDEO_GEN,
    STYLE_PAGE_PREFIX, STYLE_SELECT_PREFIX
)
from bot.utils.job_id import generate_job_id
from bot.utils.telegram import get_telegram_file_url
from bot.utils.user import is_vip_user
from bot.config import BOT_PUBLIC_USERNAME

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.content_type == "photo")
async def handle_photo(message: Message, bot: Bot) -> None:
    """Handle photo messages and show image action menu or process target photo."""
    user_id = message.from_user.id
    chat_id = str(message.chat.id)
    
    logger.info(f"Photo received from user {user_id}")
    
    try:
        # Check if user has a pending photo swap job
        bot_jobs_photo_repo = BotJobsPhotoRepository()
        pending_job = await bot_jobs_photo_repo.get_job_by_chat_id(chat_id)
        
        if pending_job:
            # This is a target photo for photo swap
            await handle_target_photo(message, bot, pending_job)
            return
        
        # Regular photo - show image action menu
        user_repo = UserRepository()
        user = await user_repo.get_user(user_id)
        user_language = user.get("language", "en") if user else "en"
        
        # Send image action prompt with keyboard
        await message.answer(
            get_text(user_language, "image_actions.prompt"),
            reply_markup=kb_image_actions()
        )
        
    except Exception as e:
        logger.error(f"Error handling photo from user {user_id}: {e}")
        await message.answer("Error processing your photo. Please try again.")

async def handle_target_photo(message: Message, bot: Bot, pending_job: BotJobsPhoto) -> None:
    """Handle target photo for photo swap."""
    user_id = message.from_user.id
    chat_id = str(message.chat.id)
    
    try:
        # Get the highest quality photo
        photo = message.photo[-1]
        file_id = photo.file_id
        
        # Get Telegram file URL
        target_photo_url = await get_telegram_file_url(bot, file_id)
        if not target_photo_url:
            await message.answer("Failed to process target photo. Please try again.")
            return
        
        # Update the job with target photo
        bot_jobs_photo_repo = BotJobsPhotoRepository()
        await bot_jobs_photo_repo.update_target_photo(chat_id, target_photo_url)
        
        logger.info(f"Updated BotJobsPhoto job for user {user_id} with target photo")
        
        # Get user's language preference
        user_repo = UserRepository()
        user = await user_repo.get_user(user_id)
        user_language = user.get("language", "en") if user else "en"
        
        # Send confirmation message
        await message.answer(
            "✅ Target photo received! Your photo swap job is now in review.",
            reply_markup=kb_image_actions()
        )
        
    except Exception as e:
        logger.error(f"Error handling target photo for user {user_id}: {e}")
        await message.answer("Error processing your target photo. Please try again.")

@router.callback_query(F.data == IMAGE_GENERATE)
async def handle_generate_image(callback: CallbackQuery) -> None:
    """Handle Generate Image button - show style selection with n.jpg."""
    user_id = callback.from_user.id
    
    logger.info(f"Generate Image selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Send style selection message with n.jpg attachment
    photo_file = FSInputFile("bot/src/n.jpg")
    dynamic_keyboard = await kb_dynamic_style_selection(page=1)
    await callback.message.answer_photo(
        photo=photo_file,
        caption=get_text(user_language, "style_selection.prompt"),
        reply_markup=dynamic_keyboard
    )
    
    await callback.answer()


@router.callback_query(F.data == IMAGE_FACE_SWAP)
async def handle_face_swap(callback: CallbackQuery) -> None:
    """Handle Face Swap button - show face swap options."""
    user_id = callback.from_user.id
    logger.info(f"Face Swap selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Update the message to show face swap options
    await callback.message.edit_caption(
        caption=get_text(user_language, "face_swap.prompt"),
        reply_markup=kb_face_swap_options()
    )
    
    await callback.answer()

@router.callback_query(F.data == IMAGE_VIDEO_GEN)
async def handle_video_generation(callback: CallbackQuery) -> None:
    """Handle Generate Video button - placeholder."""
    user_id = callback.from_user.id
    logger.info(f"Generate Video selected by user {user_id}")
    
    await callback.answer("Video Generation feature coming soon!")

@router.callback_query(F.data.startswith(STYLE_PAGE_PREFIX))
async def handle_style_pagination(callback: CallbackQuery) -> None:
    """Handle style pagination."""
    user_id = callback.from_user.id
    page_str = callback.data.replace(STYLE_PAGE_PREFIX, "")
    
    try:
        page = int(page_str)
        logger.info(f"Style page {page} selected by user {user_id}")
        
        # Get user's language preference
        user_repo = UserRepository()
        user = await user_repo.get_user(user_id)
        user_language = user.get("language", "en") if user else "en"
        
        # Update the message with new page
        dynamic_keyboard = await kb_dynamic_style_selection(page=page)
        await callback.message.edit_caption(
            caption=get_text(user_language, "style_selection.prompt"),
            reply_markup=dynamic_keyboard
        )
        
    except ValueError:
        logger.error(f"Invalid page number: {page_str}")
        await callback.answer("Invalid page number")
        return
    
    await callback.answer()

@router.callback_query(F.data.startswith(STYLE_SELECT_PREFIX))
async def handle_style_selection(callback: CallbackQuery, bot: Bot) -> None:
    """Handle style selection."""
    user_id = callback.from_user.id
    style_id = callback.data.replace(STYLE_SELECT_PREFIX, "")
    
    logger.info(f"Style '{style_id}' selected by user {user_id}")
    
    try:
        # Get user data
        user_repo = UserRepository()
        user = await user_repo.get_user(user_id)
        if not user:
            await callback.answer("User not found. Please start the bot first.")
            return
        
        # Get photo from the message
        if not callback.message.photo:
            await callback.answer("No photo found in message.")
            return
        
        # Get the highest quality photo
        photo = callback.message.photo[-1]
        file_id = photo.file_id
        
        # Get Telegram file URL
        photo_url = await get_telegram_file_url(bot, file_id)
        if not photo_url:
            await callback.answer("Failed to process photo. Please try again.")
            return
        
        # Create ProcessImg job
        process_img_repo = ProcessImgRepository()
        job: ProcessImg = {
            "_id": ObjectId(),
            "file_id": file_id,
            "bot": BOT_PUBLIC_USERNAME or "unknown_bot",
            "chat_id": str(callback.message.chat.id),
            "caption": style_id,
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            "queue": "vip" if is_vip_user(user) else "free",
            "time_start": None,
            "output_url": None,
            "time_taken": None
        }
        
        job_id = await process_img_repo.create_job(job)
        logger.info(f"Created ProcessImg job {job_id} for user {user_id} with style {style_id}")
        
        # Increment the count for the selected node
        node_repo = NodeRepository()
        await node_repo.increment_count(style_id)
        logger.info(f"Incremented count for node with other_text: {style_id}")
        
        await callback.answer(f"Style '{style_id}' selected! Job created successfully.")
        
    except Exception as e:
        logger.error(f"Error creating ProcessImg job for user {user_id}: {e}")
        await callback.answer("Error processing your request. Please try again.")

@router.callback_query(F.data == "current_page")
async def handle_current_page(callback: CallbackQuery) -> None:
    """Handle current page button click - do nothing."""
    await callback.answer()

@router.callback_query(F.data == "explore_styles")
async def handle_explore_styles(callback: CallbackQuery) -> None:
    """Handle Explore +1500 Options button - placeholder."""
    user_id = callback.from_user.id
    logger.info(f"Explore styles selected by user {user_id}")
    
    await callback.answer("Explore styles feature coming soon!")

@router.callback_query(F.data == "bot_list")
async def handle_bot_list(callback: CallbackQuery) -> None:
    """Handle BOT LIST button - placeholder."""
    user_id = callback.from_user.id
    logger.info(f"Bot list selected by user {user_id}")
    
    await callback.answer("Bot list feature coming soon!")

@router.callback_query(F.data == "photo_swap")
async def handle_photo_swap(callback: CallbackQuery, bot: Bot) -> None:
    """Handle Photo Swap button - create job and request target photo."""
    user_id = callback.from_user.id
    logger.info(f"Photo Swap selected by user {user_id}")
    
    try:
        # Get user data
        user_repo = UserRepository()
        user = await user_repo.get_user(user_id)
        if not user:
            await callback.answer("User not found. Please start the bot first.")
            return
        
        # Get user's language preference
        user_language = user.get("language", "en")
        
        # Get photo from the message
        if not callback.message.photo:
            await callback.answer("No photo found in message.")
            return
        
        # Get the highest quality photo
        photo = callback.message.photo[-1]
        file_id = photo.file_id
        
        # Get Telegram file URL
        photo_url = await get_telegram_file_url(bot, file_id)
        if not photo_url:
            await callback.answer("Failed to process photo. Please try again.")
            return
        
        # Create BotJobsPhoto job
        bot_jobs_photo_repo = BotJobsPhotoRepository()
        job: BotJobsPhoto = {
            "_id": ObjectId(),
            "chat_id": str(callback.message.chat.id),
            "status": "pending",
            "job_id": generate_job_id(),
            "bot": BOT_PUBLIC_USERNAME or "unknown_bot",
            "photo_url": photo_url,
            "target_photo_url": None,
            "vip": is_vip_user(user),
            "created_at": datetime.now(timezone.utc),
            "output_url": None,
            "time_taken": None
        }
        
        job_id = await bot_jobs_photo_repo.create_job(job)
        logger.info(f"Created BotJobsPhoto job {job_id} for user {user_id}")
        
        # Update the message to request target photo
        await callback.message.edit_caption(
            caption=get_text(user_language, "photo_swap.prompt"),
            reply_markup=kb_photo_swap_options()
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error creating BotJobsPhoto job for user {user_id}: {e}")
        await callback.answer("Error processing your request. Please try again.")

@router.callback_query(F.data == "video_swap")
async def handle_video_swap(callback: CallbackQuery, bot: Bot) -> None:
    """Handle Video Swap button - store source photo and show video options."""
    user_id = callback.from_user.id
    logger.info(f"Video Swap selected by user {user_id}")
    
    try:
        # Get user data
        user_repo = UserRepository()
        user = await user_repo.get_user(user_id)
        if not user:
            await callback.answer("User not found. Please start the bot first.")
            return
        
        # Get user's language preference
        user_language = user.get("language", "en")
        
        # Get photo from the message
        if not callback.message.photo:
            await callback.answer("No photo found in message.")
            return
        
        # Get the highest quality photo
        photo = callback.message.photo[-1]
        file_id = photo.file_id
        
        # Get Telegram file URL
        photo_url = await get_telegram_file_url(bot, file_id)
        if not photo_url:
            await callback.answer("Failed to process photo. Please try again.")
            return
        
        # Store the source photo for later use with deep links
        # We'll create a temporary job that can be completed when user clicks a video link
        bot_jobs_video_repo = BotJobsVideoRepository()
        temp_job: BotJobsVideo = {
            "_id": ObjectId(),
            "chat_id": str(callback.message.chat.id),
            "status": "pending",
            "job_id": generate_job_id(),
            "photo_url": photo_url,
            "video_url": "",  # Will be filled when video is selected
            "video_size": 0,  # Will be filled when video is selected
            "duration": 0,    # Will be filled when video is selected
            "vip": is_vip_user(user),
            "bot": BOT_PUBLIC_USERNAME or "unknown_bot",
            "created_at": datetime.now(timezone.utc),
            "output_url": None,
            "time_taken": None
        }
        
        job_id = await bot_jobs_video_repo.create_job(temp_job)
        logger.info(f"Created temporary BotJobsVideo job {job_id} for user {user_id}")
        
        # Update the message to show video options
        await callback.message.edit_caption(
            caption=get_text(user_language, "video_swap.prompt"),
            reply_markup=kb_video_swap_options()
        )
        
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error creating temporary BotJobsVideo job for user {user_id}: {e}")
        await callback.answer("Error processing your request. Please try again.")

@router.callback_query(F.data == "back_to_face_swap")
async def handle_back_to_face_swap(callback: CallbackQuery) -> None:
    """Handle Back button - return to face swap options."""
    user_id = callback.from_user.id
    logger.info(f"Back to face swap selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Update the message to show face swap options again
    await callback.message.edit_caption(
        caption=get_text(user_language, "face_swap.prompt"),
        reply_markup=kb_face_swap_options()
    )
    
    await callback.answer()

@router.callback_query(F.data == "cancel_operation")
async def handle_cancel_operation(callback: CallbackQuery) -> None:
    """Handle Cancel button - return to image actions."""
    user_id = callback.from_user.id
    logger.info(f"Cancel operation selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Update the message to show image actions again
    await callback.message.edit_caption(
        caption=get_text(user_language, "image_actions.prompt"),
        reply_markup=kb_image_actions()
    )
    
    await callback.answer()

@router.callback_query(F.data == "reels_18_plus")
async def handle_reels_18_plus(callback: CallbackQuery) -> None:
    """Handle Reels 18+ button - placeholder."""
    user_id = callback.from_user.id
    logger.info(f"Reels 18+ selected by user {user_id}")
    
    await callback.answer("Reels 18+ feature coming soon!")

@router.callback_query(F.data == "back_to_actions")
async def handle_back_to_actions(callback: CallbackQuery) -> None:
    """Handle Back button - return to image actions."""
    user_id = callback.from_user.id
    logger.info(f"Back to actions selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Update the message to show image actions again
    await callback.message.edit_caption(
        caption=get_text(user_language, "image_actions.prompt"),
        reply_markup=kb_image_actions()
    )
    
    await callback.answer()
