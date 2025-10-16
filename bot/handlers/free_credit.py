"""Free credit handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.services.daily import DailyService
from bot.keyboards import kb_free_credit
from bot.texts import FREE_CREDIT_TITLE, FREE_CREDIT_TEXT, DAILY_CHECKIN_SUCCESS, DAILY_CHECKIN_COOLDOWN
from bot.languages import get_text
from bot.db.repositories import UserRepository
from bot.callbacks import *

logger = logging.getLogger(__name__)
router = Router()

async def free_credit_command(message: Message) -> None:
    """Handle Get Free Credit command."""
    user_id = message.from_user.id
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Format free credit text using language system
    free_credit_text = f"{get_text(user_language, 'free_credit.title')}\n\n{get_text(user_language, 'free_credit.text')}"
    await message.answer(free_credit_text, reply_markup=kb_free_credit())

@router.callback_query(F.data == INVITE_FRIENDS)
async def invite_friends(callback: CallbackQuery) -> None:
    """Handle invite friends button."""
    from bot.db.repositories import ReferralRepository
    from bot.services.referrals import ReferralService
    from bot.languages import get_text
    from bot.keyboards import kb_affiliate
    from bot.config import BOT_PUBLIC_USERNAME
    
    user_id = callback.from_user.id
    
    # Get user's language preference
    from bot.db.repositories import UserRepository
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    referral_repo = ReferralRepository()
    referral_service = ReferralService()
    
    # Get referral count
    referral_count = await referral_repo.get_referral_count(user_id)
    
    # Get bot username from config
    bot_username = BOT_PUBLIC_USERNAME or "your_bot"
    
    # Generate referral link
    referral_link = await referral_service.get_referral_link(user_id, bot_username)
    
    # Format affiliate text using language system
    affiliate_text = f"{get_text(user_language, 'affiliate.title')}\n\n{get_text(user_language, 'affiliate.text').format(ref_link=referral_link, count=referral_count)}"
    
    await callback.message.answer(affiliate_text, reply_markup=kb_affiliate())
    await callback.answer()

@router.callback_query(F.data == DAILY_CHECKIN)
async def daily_checkin(callback: CallbackQuery) -> None:
    """Handle daily check-in."""
    user_id = callback.from_user.id
    daily_service = DailyService()
    
    # Check if user can check in
    can_checkin, remaining_time = await daily_service.can_checkin(user_id)
    
    if can_checkin:
        # Perform check-in
        success = await daily_service.perform_checkin(user_id)
        if success:
            await callback.answer(DAILY_CHECKIN_SUCCESS)
        else:
            await callback.answer("Error performing check-in. Please try again.")
    else:
        # Show cooldown message
        cooldown_msg = DAILY_CHECKIN_COOLDOWN.format(time=remaining_time)
        await callback.answer(cooldown_msg)

@router.callback_query(F.data == "back_profile")
async def back_to_profile(callback: CallbackQuery) -> None:
    """Handle back to profile."""
    from bot.db.repositories import UserRepository, ReferralRepository
    from bot.languages import get_text
    from bot.keyboards import kb_profile_back
    from bot.utils.formatting import format_currency
    
    user_id = callback.from_user.id
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    if not user:
        await callback.message.answer("User not found. Please use /start first.")
        await callback.answer()
        return
    
    # Get referral count
    referral_repo = ReferralRepository()
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
    
    await callback.message.answer(profile_text, reply_markup=kb_profile_back())
    await callback.answer()


