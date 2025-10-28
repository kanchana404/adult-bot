"""Start command handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from datetime import timedelta, timezone
from bot.db.repositories import UserRepository, BotJobsVideoRepository
from bot.db.models import User
from bot.services.referrals import ReferralService
from bot.services.economy import EconomyService
from bot.keyboards import kb_main_menu, kb_important_notice
from bot.admin_keyboards import kb_admin_menu
from bot.texts import WELCOME_NEW, WELCOME_BACK, IMPORTANT_NOTICE
from bot.languages import get_text
from bot.utils.time import utc_now
from bot.utils.user import is_admin_user

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def start_command(message: Message) -> None:
    """Handle /start command with optional referral payload."""
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    logger.info(f"Start command received from user {user_id} (@{username})")
    logger.info(f"Message text: {message.text}")
    
    user_repo = UserRepository()
    referral_service = ReferralService()
    
    # Check if user exists
    user = await user_repo.get_user(user_id)
    logger.info(f"User exists check: {user is not None}")
    
    if not user:
        logger.info(f"Creating new user: {user_id}")
        # Create new user
        current_time = utc_now()
        new_user: User = {
            "_id": user_id,
            "created_at": current_time,
            "account_id": user_id,
            "balance_usd": "0.10",
            "tickets": 1,
            "vip_tickets": 0,
            "lucky_spins": 0,
            "referrer_id": None,
            "referral_count": 0,
            "referral_ticket_earned": "0.00",
            "accepted_terms": False,
            "last_daily_checkin_at": None,
            "language": "en",
            "last_activity": current_time
        }
        
        # Check for referral payload or video deep link
        logger.info(f"Checking payload in message: '{message.text}'")
        referrer_id = None
        video_id = None
        
        if message.text and len(message.text.split()) > 1:
            payload = message.text.split()[1]
            
            # Check if it's a video deep link
            if payload.startswith("idvideo_"):
                video_id = payload.replace("idvideo_", "")
                logger.info(f"Video deep link detected: video_id={video_id}, user_id={user_id}")
            else:
                # Try to parse as referral ID
                try:
                    referrer_id = int(payload)
                    logger.info(f"Referral detected: referrer_id={referrer_id}, new_user_id={user_id}")
                    if referrer_id != user_id:  # Can't refer yourself
                        new_user["referrer_id"] = referrer_id
                        logger.info(f"Setting referrer_id in new user: {referrer_id}")
                    else:
                        logger.info(f"User tried to refer themselves: {user_id}")
                        referrer_id = None
                except (ValueError, IndexError) as e:
                    logger.error(f"Invalid payload: {message.text}, error: {e}")
                    referrer_id = None
        else:
            logger.info(f"No payload found in message: '{message.text}'")
        
        # Create user first
        await user_repo.create_user(new_user)
        logger.info(f"User created in database: {user_id}")
        
        # Process referral AFTER user is created
        if referrer_id:
            logger.info(f"Processing referral after user creation: {referrer_id} -> {user_id}")
            success = await referral_service.process_referral(referrer_id, user_id)
            logger.info(f"Referral processing result: {success}")
        
        # Process video deep link if present
        if video_id:
            logger.info(f"Processing video deep link: video_id={video_id}, user_id={user_id}")
            await process_video_deep_link(user_id, video_id, message)
        
        # Get user's language for welcome message
        user_language = new_user.get("language", "en")
        
        # Check if user is admin
        if is_admin_user(user_id):
            # Admin welcome message
            admin_welcome_text = f"""🔧 <b>ADMIN PANEL</b> 🔧

Welcome back, Admin!

👤 <b>Your Account:</b>
• Account ID: {new_user["account_id"]}
• Balance: ${new_user["balance_usd"]}
• Tickets: {new_user["tickets"]} 🎟️
• VIP Tickets: {new_user["vip_tickets"]} ⭐
• Lucky Spins: {new_user["lucky_spins"]} 🍀

🎛️ <b>Admin Features:</b>
• User Status & Analytics
• Revenue Tracking
• Button Management
• Bot Statistics

Use the buttons below to access admin functions."""
            
            # Send video with admin welcome message
            video_file = FSInputFile("bot/src/data.mp4")
            welcome_msg = await message.answer_video(
                video=video_file,
                caption=admin_welcome_text,
                reply_markup=kb_admin_menu()
            )
        else:
            # Regular user welcome message
            welcome_text = get_text(user_language, "welcome.new").format(
                account_id=new_user["account_id"],
                balance=new_user["balance_usd"],
                tickets=new_user["tickets"],
                vip=new_user["vip_tickets"],
                lucky=new_user["lucky_spins"]
            )
            
            # Send video with welcome message as caption
            video_file = FSInputFile("bot/src/data.mp4")
            welcome_msg = await message.answer_video(
                video=video_file,
                caption=welcome_text,
                reply_markup=kb_main_menu(user_language)
            )
        
        # Pin the welcome message
        try:
            await welcome_msg.pin()
            logger.info(f"Welcome message pinned for new user: {user_id}")
        except Exception as e:
            logger.warning(f"Failed to pin welcome message for user {user_id}: {e}")
        
        logger.info(f"New user created and welcome message sent: {user_id} (@{username})")
    else:
        logger.info(f"Existing user found: {user_id}")
        
        # Check for video deep link in existing user
        video_id = None
        if message.text and len(message.text.split()) > 1:
            payload = message.text.split()[1]
            if payload.startswith("idvideo_"):
                video_id = payload.replace("idvideo_", "")
                logger.info(f"Video deep link detected for existing user: video_id={video_id}, user_id={user_id}")
        
        # Process video deep link if present
        if video_id:
            logger.info(f"Processing video deep link for existing user: video_id={video_id}, user_id={user_id}")
            await process_video_deep_link(user_id, video_id, message)
        
        # Existing user - check if inactive for 1+ hour
        user_language = user.get("language", "en")
        last_activity = user.get("last_activity")
        current_time = utc_now()
        
        logger.info(f"User {user_id} activity check: last_activity from DB: {last_activity}")
        
        # Check if user has been inactive for more than 1 hour
        if last_activity is None:
            is_inactive = True
            logger.info(f"User {user_id} has no last_activity, marking as inactive")
        else:
            # Make both datetimes timezone-aware for comparison
            if last_activity.tzinfo is None:
                last_activity_aware = last_activity.replace(tzinfo=timezone.utc)
            else:
                last_activity_aware = last_activity
            
            time_diff = current_time - last_activity_aware
            is_inactive = time_diff > timedelta(hours=1)
            
            logger.info(f"User {user_id} activity check: last_activity={last_activity_aware}, current_time={current_time}, time_diff={time_diff}, is_inactive={is_inactive}")
        
        if is_inactive:
            logger.info(f"User {user_id} has been inactive for 1+ hours, sending important notice")
            
            # Send important notice message
            notice_text = get_text(user_language, "important_notice.text")
            notice_msg = await message.answer(notice_text, reply_markup=kb_important_notice())
            
            # Pin the notice message
            try:
                await notice_msg.pin()
                logger.info(f"Important notice message pinned for user: {user_id}")
            except Exception as e:
                logger.warning(f"Failed to pin notice message for user {user_id}: {e}")
        
        # Send welcome back message with video
        if is_admin_user(user_id):
            # Admin welcome message
            admin_welcome_text = f"""🔧 <b>ADMIN PANEL</b> 🔧

Welcome back, Admin!

👤 <b>Your Account:</b>
• Account ID: {user["account_id"]}
• Balance: ${user["balance_usd"]}
• Tickets: {user["tickets"]} 🎟️
• VIP Tickets: {user["vip_tickets"]} ⭐
• Lucky Spins: {user["lucky_spins"]} 🍀

🎛️ <b>Admin Features:</b>
• User Status & Analytics
• Revenue Tracking
• Button Management
• Bot Statistics

Use the buttons below to access admin functions."""
            
            # Send video with admin welcome message
            video_file = FSInputFile("bot/src/data.mp4")
            welcome_msg = await message.answer_video(
                video=video_file,
                caption=admin_welcome_text,
                reply_markup=kb_admin_menu()
            )
        else:
            # Regular user welcome message
            welcome_text = get_text(user_language, "welcome.back").format(
                account_id=user["account_id"],
                balance=user["balance_usd"],
                tickets=user["tickets"],
                vip=user["vip_tickets"],
                lucky=user["lucky_spins"]
            )
            
            # Send video with welcome message as caption
            video_file = FSInputFile("bot/src/data.mp4")
            welcome_msg = await message.answer_video(
                video=video_file,
                caption=welcome_text,
                reply_markup=kb_main_menu(user_language)
            )
        
        # Pin the welcome message
        try:
            await welcome_msg.pin()
            logger.info(f"Welcome message pinned for existing user: {user_id}")
        except Exception as e:
            logger.warning(f"Failed to pin welcome message for user {user_id}: {e}")
        
        # Update last activity
        await user_repo.update_last_activity(user_id)
        
        logger.info(f"Welcome back message sent to existing user: {user_id} (@{username})")

async def process_video_deep_link(user_id: int, video_id: str, message: Message) -> None:
    """Process video deep link for face swap."""
    try:
        bot_jobs_video_repo = BotJobsVideoRepository()
        
        # Look up the video data
        video_data = await bot_jobs_video_repo.get_video_by_id(video_id)
        if not video_data:
            logger.warning(f"Video data not found for video_id: {video_id}")
            await message.answer("❌ Video not found. Please try a different link.")
            return
        
        # Check if user has a pending video job with a photo
        chat_id = str(message.chat.id)
        pending_job = await bot_jobs_video_repo.get_job_by_id(video_id)
        
        if pending_job and pending_job.get("photo_url") and pending_job.get("status") == "pending":
            # Update the existing job with video data
            # We need to update the job with video information
            from bot.db.mongo import get_database
            collection = get_database().bot_jobs_video
            await collection.update_one(
                {"job_id": video_id},
                {
                    "$set": {
                        "status": "processing",
                        "video_url": video_data.get("video_url", ""),
                        "video_size": video_data.get("video_size", 0),
                        "duration": video_data.get("duration", 0)
                    }
                }
            )
            
            logger.info(f"Updated video job {video_id} with video data for user {user_id}")
            await message.answer("✅ Video selected! Your face swap job is now processing.")
        else:
            # User needs to send a photo first
            logger.info(f"User {user_id} needs to send photo first for video {video_id}")
            await message.answer("📸 Please send a photo first to perform the face swap with this video.")
            
    except Exception as e:
        logger.error(f"Error processing video deep link for user {user_id}, video_id {video_id}: {e}")
        await message.answer("❌ Error processing video link. Please try again.")


