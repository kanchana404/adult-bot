"""Keyboard builders for the bot."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.callbacks import (
    TELEGRAM_STARS, CRYPTO, PAYPAL, TOPUP, 
    STAR_PACKAGE_PREFIX, VERIFY_PAYMENT_PREFIX, 
    CHECK_PAYMENT_HISTORY, CRYPTO_PACKAGE_PREFIX,
    CHECK_CRYPTO_INVOICE_PREFIX, CREATE_CUSTOM_CRYPTO,
    CHECK_CRYPTO_HISTORY, BACK_PROFILE, BACK_MAIN,
    UNIFIED_PAYMENT_HISTORY, UNIFIED_PAYMENT_PAGE_PREFIX,
    SHARE_LINK, INVITE_FRIENDS, DAILY_CHECKIN, VIEW_TERMS, AGREE_TERMS
)
from bot.languages import get_text

def kb_main_menu(language: str = "en") -> ReplyKeyboardMarkup:
    """Main menu keyboard with language support."""
    keyboard = [
        [
            KeyboardButton(text=get_text(language, "main_menu.profile")),
            KeyboardButton(text=get_text(language, "main_menu.language")),
            KeyboardButton(text=get_text(language, "main_menu.topup"))
        ],
        [
            KeyboardButton(text=get_text(language, "main_menu.affiliate")),
            KeyboardButton(text=get_text(language, "main_menu.free_credit")),
            KeyboardButton(text=get_text(language, "main_menu.terms"))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def kb_profile_back() -> InlineKeyboardMarkup:
    """Profile back button."""
    keyboard = [
        [InlineKeyboardButton(text="⬅️ Back to Main", callback_data=BACK_MAIN)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_topup_methods() -> InlineKeyboardMarkup:
    """Top up payment methods keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="⭐ Telegram Star Payment", callback_data=TELEGRAM_STARS)],
        [InlineKeyboardButton(text="🪙 Crypto", callback_data=CRYPTO)],
        [InlineKeyboardButton(text="💳 PayPal", callback_data=PAYPAL)],
        [InlineKeyboardButton(text="📊 Payment History", callback_data=UNIFIED_PAYMENT_HISTORY)],
        [InlineKeyboardButton(text="⬅️ Back to Profile", callback_data=BACK_PROFILE)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_star_packages() -> InlineKeyboardMarkup:
    """Telegram Stars package selection keyboard."""
    from bot.services.payments import PAYMENT_PACKAGES
    
    keyboard = []
    for i, pkg in enumerate(PAYMENT_PACKAGES):
        button_text = f"{pkg['label']} - {pkg['stars']} ⭐ ({pkg['tickets']} 🎟️)"
        keyboard.append([InlineKeyboardButton(
            text=button_text, 
            callback_data=f"{STAR_PACKAGE_PREFIX}{i}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="⬅️ Back", callback_data=TOPUP)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_payment_verify(payment_url: str, payload: str) -> InlineKeyboardMarkup:
    """Payment verification keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="💳 Pay with Stars", url=payment_url)],
        [InlineKeyboardButton(text="✅ I Paid - Verify", callback_data=f"{VERIFY_PAYMENT_PREFIX}{payload}")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data=TELEGRAM_STARS)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_crypto_packages() -> InlineKeyboardMarkup:
    """Crypto payment package selection keyboard."""
    from bot.services.payments import CRYPTO_PACKAGES
    
    keyboard = []
    for i, pkg in enumerate(CRYPTO_PACKAGES):
        button_text = f"{pkg['label']} - {pkg['amount']} {pkg['currency']} ({pkg['tickets']} 🎟️)"
        keyboard.append([InlineKeyboardButton(
            text=button_text, 
            callback_data=f"{CRYPTO_PACKAGE_PREFIX}{i}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="💰 Custom Amount", callback_data=CREATE_CUSTOM_CRYPTO)])
    keyboard.append([InlineKeyboardButton(text="⬅️ Back", callback_data=TOPUP)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_crypto_invoice_verify(payment_url: str, invoice_id: str) -> InlineKeyboardMarkup:
    """Crypto invoice verification keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="💳 Pay Invoice", url=payment_url)],
        [InlineKeyboardButton(text="✅ Check Status", callback_data=f"{CHECK_CRYPTO_INVOICE_PREFIX}{invoice_id}")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data=CRYPTO)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_affiliate() -> InlineKeyboardMarkup:
    """Affiliate keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="🔗 Share Link", callback_data=SHARE_LINK)],
        [InlineKeyboardButton(text="⬅️ Back to Profile", callback_data=BACK_PROFILE)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_free_credit() -> InlineKeyboardMarkup:
    """Free credit keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="👥 Invite Friends", callback_data=INVITE_FRIENDS)],
        [InlineKeyboardButton(text="✅ Daily Check-in", callback_data=DAILY_CHECKIN)],
        [InlineKeyboardButton(text="⬅️ Back to Profile", callback_data=BACK_PROFILE)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_terms() -> InlineKeyboardMarkup:
    """Terms keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="📜 View Terms of Service", callback_data=VIEW_TERMS)],
        [InlineKeyboardButton(text="✅ I Agree", callback_data=AGREE_TERMS)],
        [InlineKeyboardButton(text="⬅️ Back to Profile", callback_data=BACK_PROFILE)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_unified_payment_history(page: int = 1, has_previous: bool = False, has_next: bool = False) -> InlineKeyboardMarkup:
    """Unified payment history keyboard with pagination."""
    keyboard = []
    
    # Pagination buttons
    if has_previous or has_next:
        pagination_row = []
        if has_previous:
            pagination_row.append(InlineKeyboardButton(
                text="⬅️ Previous", 
                callback_data=f"{UNIFIED_PAYMENT_PAGE_PREFIX}{page - 1}"
            ))
        if has_next:
            pagination_row.append(InlineKeyboardButton(
                text="Next ➡️", 
                callback_data=f"{UNIFIED_PAYMENT_PAGE_PREFIX}{page + 1}"
            ))
        keyboard.append(pagination_row)
    
    # Back button
    keyboard.append([InlineKeyboardButton(text="⬅️ Back to Top Up", callback_data=TOPUP)])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_important_notice() -> InlineKeyboardMarkup:
    """Important notice keyboard with backup bot button."""
    keyboard = [
        [InlineKeyboardButton(text="Backup Bot 🎟", url="https://t.me/Onii1BackupBot")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

