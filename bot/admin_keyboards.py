"""Admin keyboard builders for the bot."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_admin_menu() -> InlineKeyboardMarkup:
    """Admin menu keyboard with admin-specific features."""
    keyboard = [
        [
            InlineKeyboardButton(text="👥 User Status", callback_data="admin_user_status"),
            InlineKeyboardButton(text="💰 Revenue Status", callback_data="admin_revenue_status")
        ],
        [
            InlineKeyboardButton(text="🎨 Button Management", callback_data="admin_button_management"),
            InlineKeyboardButton(text="📊 Bot Statistics", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_button_management() -> InlineKeyboardMarkup:
    """Button management keyboard for admins."""
    keyboard = [
        [
            InlineKeyboardButton(text="📋 List All Buttons", callback_data="admin_list_buttons"),
            InlineKeyboardButton(text="➕ Add New Button", callback_data="admin_add_button")
        ],
        [
            InlineKeyboardButton(text="🗑️ Delete Button", callback_data="admin_delete_button"),
            InlineKeyboardButton(text="📈 Button Stats", callback_data="admin_button_stats")
        ],
        [
            InlineKeyboardButton(text="⬅️ Back to Admin Menu", callback_data="admin_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
