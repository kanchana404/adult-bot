"""Affiliate handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.db.repositories import ReferralRepository
from bot.services.referrals import ReferralService
from bot.keyboards import kb_affiliate
from bot.texts import AFFILIATE_TITLE, AFFILIATE_TEXT
from bot.languages import get_text
from bot.db.repositories import UserRepository
from bot.config import BOT_PUBLIC_USERNAME
from bot.callbacks import *

logger = logging.getLogger(__name__)
router = Router()

async def affiliate_command(message: Message) -> None:
    """Handle Affiliate money command."""
    user_id = message.from_user.id
    
    # Get user's language preference
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
    
    await message.answer(affiliate_text, reply_markup=kb_affiliate())

@router.callback_query(F.data == SHARE_LINK)
async def share_link(callback: CallbackQuery) -> None:
    """Handle share link button."""
    user_id = callback.from_user.id
    
    # Get bot username from config
    bot_username = BOT_PUBLIC_USERNAME or "your_bot"
    
    # Generate referral link
    referral_service = ReferralService()
    referral_link = await referral_service.get_referral_link(user_id, bot_username)
    
    # Send the link as a new message for easy sharing
    await callback.message.answer(f"🔗 Your referral link:\n{referral_link}")
    await callback.answer("Referral link sent!")

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


