"""Top up handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.db.repositories import UserRepository
from bot.services.payments import PaymentService
from bot.keyboards import kb_topup_methods
from bot.texts import TOPUP_HEADER
from bot.languages import get_text
from bot.utils.formatting import format_currency
from bot.callbacks import (
    TELEGRAM_STARS, CRYPTO, PAYPAL, TOPUP, 
    STAR_PACKAGE_PREFIX, VERIFY_PAYMENT_PREFIX, 
    CHECK_PAYMENT_HISTORY, CRYPTO_PACKAGE_PREFIX,
    CHECK_CRYPTO_INVOICE_PREFIX, CHECK_CRYPTO_HISTORY,
    CREATE_CUSTOM_CRYPTO, UNIFIED_PAYMENT_HISTORY, UNIFIED_PAYMENT_PAGE_PREFIX
)

logger = logging.getLogger(__name__)
router = Router()

async def topup_command(message: Message) -> None:
    """Handle Top up Credit command."""
    user_id = message.from_user.id
    
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    
    if not user:
        await message.answer("User not found. Please use /start first.")
        return
    
    # Get user's language preference
    user_language = user.get("language", "en")
    
    # Format top up text using language system
    topup_text = get_text(user_language, "topup.title").format(
        account_id=user["account_id"],
        balance=format_currency(user["balance_usd"]),
        tickets=user["tickets"],
        vip=user["vip_tickets"],
        lucky=user["lucky_spins"]
    )
    
    await message.answer(topup_text, reply_markup=kb_topup_methods())

@router.callback_query(F.data == TELEGRAM_STARS)
async def telegram_stars_payment(callback: CallbackQuery) -> None:
    """Handle Telegram Stars payment."""
    payment_service = PaymentService()
    await payment_service.handle_telegram_star_payment(callback)

@router.callback_query(F.data == CRYPTO)
async def crypto_payment(callback: CallbackQuery) -> None:
    """Handle crypto payment."""
    payment_service = PaymentService()
    await payment_service.handle_crypto_payment(callback)

@router.callback_query(F.data == PAYPAL)
async def paypal_payment(callback: CallbackQuery) -> None:
    """Handle PayPal payment."""
    payment_service = PaymentService()
    await payment_service.handle_paypal_payment(callback)

@router.callback_query(F.data.startswith(STAR_PACKAGE_PREFIX))
async def star_package_selected(callback: CallbackQuery) -> None:
    """Handle star package selection."""
    package_index = int(callback.data.replace(STAR_PACKAGE_PREFIX, ""))
    payment_service = PaymentService()
    await payment_service.create_star_invoice(callback, package_index)

@router.callback_query(F.data.startswith(VERIFY_PAYMENT_PREFIX))
async def verify_payment(callback: CallbackQuery) -> None:
    """Handle payment verification."""
    payload = callback.data.replace(VERIFY_PAYMENT_PREFIX, "")
    payment_service = PaymentService()
    await payment_service.verify_payment(callback, payload)

@router.callback_query(F.data == CHECK_PAYMENT_HISTORY)
async def check_payment_history(callback: CallbackQuery) -> None:
    """Handle payment history request."""
    user_id = callback.from_user.id
    payment_service = PaymentService()
    
    history_text = await payment_service.get_payment_history(user_id)
    
    from bot.keyboards import kb_topup_methods
    await callback.answer()
    await callback.message.edit_text(history_text, reply_markup=kb_topup_methods())

@router.callback_query(F.data == TOPUP)
async def topup_callback(callback: CallbackQuery) -> None:
    """Handle top up callback (back button)."""
    user_id = callback.from_user.id
    
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    
    if not user:
        await callback.message.answer("User not found. Please use /start first.")
        await callback.answer()
        return
    
    # Get user's language preference
    user_language = user.get("language", "en")
    
    # Format top up text using language system
    topup_text = get_text(user_language, "topup.title").format(
        account_id=user["account_id"],
        balance=format_currency(user["balance_usd"]),
        tickets=user["tickets"],
        vip=user["vip_tickets"],
        lucky=user["lucky_spins"]
    )
    
    from bot.keyboards import kb_topup_methods
    await callback.answer()
    await callback.message.edit_text(topup_text, reply_markup=kb_topup_methods())

@router.callback_query(F.data.startswith(CRYPTO_PACKAGE_PREFIX))
async def crypto_package_selected(callback: CallbackQuery) -> None:
    """Handle crypto package selection."""
    package_index = int(callback.data.replace(CRYPTO_PACKAGE_PREFIX, ""))
    payment_service = PaymentService()
    await payment_service.create_crypto_invoice(callback, package_index)

@router.callback_query(F.data.startswith(CHECK_CRYPTO_INVOICE_PREFIX))
async def check_crypto_invoice(callback: CallbackQuery) -> None:
    """Handle crypto invoice status check."""
    invoice_id = callback.data.replace(CHECK_CRYPTO_INVOICE_PREFIX, "")
    payment_service = PaymentService()
    await payment_service.check_crypto_invoice_status(callback, invoice_id)

@router.callback_query(F.data == CHECK_CRYPTO_HISTORY)
async def check_crypto_history(callback: CallbackQuery) -> None:
    """Handle crypto payment history request."""
    user_id = callback.from_user.id
    payment_service = PaymentService()
    
    history_text = await payment_service.get_crypto_payment_history(user_id)
    
    from bot.keyboards import kb_topup_methods
    await callback.answer()
    await callback.message.edit_text(history_text, reply_markup=kb_topup_methods())

@router.callback_query(F.data == CREATE_CUSTOM_CRYPTO)
async def create_custom_crypto(callback: CallbackQuery) -> None:
    """Handle custom crypto invoice creation."""
    from bot.texts import CRYPTO_CUSTOM_INVOICE
    await callback.answer()
    await callback.message.edit_text(CRYPTO_CUSTOM_INVOICE)

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

@router.callback_query(F.data == UNIFIED_PAYMENT_HISTORY)
async def unified_payment_history(callback: CallbackQuery) -> None:
    """Show unified payment history."""
    from bot.keyboards import kb_unified_payment_history
    
    user_id = callback.from_user.id
    payment_service = PaymentService()
    
    # Get first page of payment history
    text, has_previous, has_next = await payment_service.get_unified_payment_history(user_id, page=1)
    
    await callback.message.edit_text(
        text,
        reply_markup=kb_unified_payment_history(page=1, has_previous=has_previous, has_next=has_next)
    )
    await callback.answer()

@router.callback_query(F.data.startswith(UNIFIED_PAYMENT_PAGE_PREFIX))
async def unified_payment_history_page(callback: CallbackQuery) -> None:
    """Handle pagination for unified payment history."""
    from bot.keyboards import kb_unified_payment_history
    
    user_id = callback.from_user.id
    payment_service = PaymentService()
    
    # Extract page number from callback data
    page_str = callback.data.replace(UNIFIED_PAYMENT_PAGE_PREFIX, "")
    try:
        page = int(page_str)
    except ValueError:
        await callback.answer("Invalid page number.", show_alert=True)
        return
    
    # Get payment history for the requested page
    text, has_previous, has_next = await payment_service.get_unified_payment_history(user_id, page=page)
    
    await callback.message.edit_text(
        text,
        reply_markup=kb_unified_payment_history(page=page, has_previous=has_previous, has_next=has_next)
    )
    await callback.answer()


