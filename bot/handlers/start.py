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
    
    user_repo = UserRepository()
    referral_service = ReferralService()
    
    # Check if user exists
    user = await user_repo.get_user(user_id)
    
    if not user:
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
        if message.text and len(message.text.split()) > 1:
            try:
                referrer_id = int(message.text.split()[1])
                if referrer_id != user_id:  # Can't refer yourself
                    new_user["referrer_id"] = referrer_id
                    # Process referral
                    await referral_service.process_referral(referrer_id, user_id)
            except (ValueError, IndexError):
                pass  # Invalid payload, ignore
        
        await user_repo.create_user(new_user)
        # Get user's language for welcome message
        user_language = new_user.get("language", "en")
        welcome_text = get_text(user_language, "welcome.new")
        await message.answer(welcome_text, reply_markup=kb_main_menu(user_language))
        logger.info(f"New user created: {user_id} (@{username})")
    else:
        # Existing user - get their language preference
        user_language = user.get("language", "en")
        welcome_text = get_text(user_language, "welcome.back")
        await message.answer(welcome_text, reply_markup=kb_main_menu(user_language))
        logger.info(f"Existing user: {user_id} (@{username})")


