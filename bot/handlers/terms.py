"""Terms handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.services.terms import TermsService
from bot.keyboards import kb_terms
from bot.texts import TERMS_TITLE, TERMS_TEXT, TERMS_ACCEPTED
from bot.languages import get_text
from bot.db.repositories import UserRepository
from bot.callbacks import *

logger = logging.getLogger(__name__)
router = Router()

async def terms_command(message: Message) -> None:
    """Handle Terms command."""
    user_id = message.from_user.id
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Format terms text using language system
    terms_text = f"{get_text(user_language, 'terms.title')}\n\n{get_text(user_language, 'terms.text')}"
    await message.answer(terms_text, reply_markup=kb_terms())

@router.callback_query(F.data == VIEW_TERMS)
async def view_terms(callback: CallbackQuery) -> None:
    """Handle view terms button."""
    await callback.answer("Terms of Service displayed above.")

@router.callback_query(F.data == AGREE_TERMS)
async def agree_terms(callback: CallbackQuery) -> None:
    """Handle agree to terms."""
    user_id = callback.from_user.id
    terms_service = TermsService()
    
    # Accept terms
    success = await terms_service.accept_terms(user_id)
    
    if success:
        await callback.answer(TERMS_ACCEPTED)
    else:
        await callback.answer("Error accepting terms. Please try again.")

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


