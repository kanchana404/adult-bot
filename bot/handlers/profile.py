"""Profile handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.db.repositories import UserRepository, ReferralRepository
from bot.services.referrals import ReferralService
from bot.keyboards import kb_profile_back
from bot.texts import PROFILE_TEXT
from bot.languages import get_text
from bot.utils.formatting import format_currency

logger = logging.getLogger(__name__)
router = Router()

async def profile_command(message: Message) -> None:
    """Handle Profile command."""
    user_id = message.from_user.id
    
    user_repo = UserRepository()
    referral_repo = ReferralRepository()
    
    # Get user data
    user = await user_repo.get_user(user_id)
    if not user:
        await message.answer("User not found. Please use /start first.")
        return
    
    # Get user's language preference
    user_language = user.get("language", "en")
    
    # Get referral count
    referral_count = await referral_repo.get_referral_count(user_id)
    
    # Format profile text using language system
    profile_text = get_text(user_language, "profile.title").format(
        account_id=user["account_id"],
        balance=format_currency(user["balance_usd"]),
        tickets=user["tickets"],
        vip=user["vip_tickets"],
        lucky=user["lucky_spins"],
        ref_tickets=float(user["referral_ticket_earned"]),
        invited=referral_count
    )
    
    await message.answer(profile_text, reply_markup=kb_profile_back())

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery) -> None:
    """Handle back to main menu."""
    from bot.keyboards import kb_main_menu
    from bot.texts import WELCOME_BACK
    from bot.languages import get_text
    from bot.db.repositories import UserRepository
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(callback.from_user.id)
    user_language = user.get("language", "en") if user else "en"
    
    # Get translated welcome text
    welcome_text = get_text(user_language, "welcome.back")
    
    # Delete the current message and send a new one with reply keyboard
    await callback.message.delete()
    await callback.message.answer(welcome_text, reply_markup=kb_main_menu(user_language))
    await callback.answer()


