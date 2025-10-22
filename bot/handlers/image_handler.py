"""Image handler for photo processing and style selection."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot.db.repositories import UserRepository
from bot.languages import get_text
from bot.keyboards import kb_image_actions, kb_style_selection, kb_face_swap_options, kb_photo_swap_options, kb_video_swap_options
from bot.texts import IMAGE_ACTION_PROMPT, STYLE_SELECTION_PROMPT
from bot.callbacks import (
    IMAGE_GENERATE, IMAGE_FACE_SWAP, IMAGE_VIDEO_GEN,
    STYLE_PAGE_PREFIX, STYLE_SELECT_PREFIX
)

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.content_type == "photo")
async def handle_photo(message: Message) -> None:
    """Handle photo messages and show image action menu."""
    user_id = message.from_user.id
    
    logger.info(f"Photo received from user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Send image action prompt with keyboard
    await message.answer(
        get_text(user_language, "image_actions.prompt"),
        reply_markup=kb_image_actions()
    )

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
    await callback.message.answer_photo(
        photo=photo_file,
        caption=get_text(user_language, "style_selection.prompt"),
        reply_markup=kb_style_selection(page=1)
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
        await callback.message.edit_caption(
            caption=get_text(user_language, "style_selection.prompt"),
            reply_markup=kb_style_selection(page=page)
        )
        
    except ValueError:
        logger.error(f"Invalid page number: {page_str}")
        await callback.answer("Invalid page number")
        return
    
    await callback.answer()

@router.callback_query(F.data.startswith(STYLE_SELECT_PREFIX))
async def handle_style_selection(callback: CallbackQuery) -> None:
    """Handle style selection."""
    user_id = callback.from_user.id
    style_id = callback.data.replace(STYLE_SELECT_PREFIX, "")
    
    logger.info(f"Style '{style_id}' selected by user {user_id}")
    
    # Placeholder response - in the future this would process the image with the selected style
    await callback.answer(f"Style '{style_id}' selected! Processing coming soon...")

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
async def handle_photo_swap(callback: CallbackQuery) -> None:
    """Handle Photo Swap button - request photo."""
    user_id = callback.from_user.id
    logger.info(f"Photo Swap selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Update the message to request photo
    await callback.message.edit_caption(
        caption=get_text(user_language, "photo_swap.prompt"),
        reply_markup=kb_photo_swap_options()
    )
    
    await callback.answer()

@router.callback_query(F.data == "video_swap")
async def handle_video_swap(callback: CallbackQuery) -> None:
    """Handle Video Swap button - request video."""
    user_id = callback.from_user.id
    logger.info(f"Video Swap selected by user {user_id}")
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Update the message to request video
    await callback.message.edit_caption(
        caption=get_text(user_language, "video_swap.prompt"),
        reply_markup=kb_video_swap_options()
    )
    
    await callback.answer()

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
