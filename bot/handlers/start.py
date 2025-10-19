"""Start command handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.db.repositories import UserRepository
from bot.db.models import User
from bot.services.referrals import ReferralService
from bot.services.economy import EconomyService
from bot.keyboards import kb_main_menu
from bot.texts import WELCOME_NEW, WELCOME_BACK
from bot.languages import get_text
from bot.utils.time import utc_now

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
        new_user: User = {
            "_id": user_id,
            "created_at": utc_now(),
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
            "language": "en"
        }
        
        # Check for referral payload
        logger.info(f"Checking referral payload in message: '{message.text}'")
        referrer_id = None
        if message.text and len(message.text.split()) > 1:
            try:
                referrer_id = int(message.text.split()[1])
                logger.info(f"Referral detected: referrer_id={referrer_id}, new_user_id={user_id}")
                if referrer_id != user_id:  # Can't refer yourself
                    new_user["referrer_id"] = referrer_id
                    logger.info(f"Setting referrer_id in new user: {referrer_id}")
                else:
                    logger.info(f"User tried to refer themselves: {user_id}")
                    referrer_id = None
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid referral payload: {message.text}, error: {e}")
                referrer_id = None
        else:
            logger.info(f"No referral payload found in message: '{message.text}'")
        
        # Create user first
        await user_repo.create_user(new_user)
        logger.info(f"User created in database: {user_id}")
        
        # Process referral AFTER user is created
        if referrer_id:
            logger.info(f"Processing referral after user creation: {referrer_id} -> {user_id}")
            success = await referral_service.process_referral(referrer_id, user_id)
            logger.info(f"Referral processing result: {success}")
        
        # Get user's language for welcome message
        user_language = new_user.get("language", "en")
        welcome_text = get_text(user_language, "welcome.new")
        await message.answer(welcome_text, reply_markup=kb_main_menu(user_language))
        logger.info(f"New user created and welcome message sent: {user_id} (@{username})")
    else:
        logger.info(f"Existing user found: {user_id}")
        # Existing user - get their language preference
        user_language = user.get("language", "en")
        welcome_text = get_text(user_language, "welcome.back")
        await message.answer(welcome_text, reply_markup=kb_main_menu(user_language))
        logger.info(f"Welcome back message sent to existing user: {user_id} (@{username})")


