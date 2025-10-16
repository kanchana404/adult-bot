"""Keyboard builders for the bot."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.callbacks import *
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
        [InlineKeyboardButton(text="⬅️ Back to Profile", callback_data=BACK_PROFILE)]
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

