"""Keyboard builders for the bot."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.callbacks import (
    TELEGRAM_STARS, CRYPTO, PAYPAL, TOPUP, 
    STAR_PACKAGE_PREFIX, VERIFY_PAYMENT_PREFIX, 
    CHECK_PAYMENT_HISTORY, CRYPTO_PACKAGE_PREFIX,
    CHECK_CRYPTO_INVOICE_PREFIX, CREATE_CUSTOM_CRYPTO,
    CHECK_CRYPTO_HISTORY, BACK_PROFILE, BACK_MAIN,
    UNIFIED_PAYMENT_HISTORY, UNIFIED_PAYMENT_PAGE_PREFIX,
    SHARE_LINK, INVITE_FRIENDS, DAILY_CHECKIN, VIEW_TERMS, AGREE_TERMS,
    IMAGE_GENERATE, IMAGE_FACE_SWAP, IMAGE_VIDEO_GEN,
    STYLE_PAGE_PREFIX, STYLE_SELECT_PREFIX
)
from bot.languages import get_text
from bot.db.repositories import NodeRepository

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

def kb_image_actions() -> InlineKeyboardMarkup:
    """Image action selection keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(text="🎨 Generate Image", callback_data=IMAGE_GENERATE),
            InlineKeyboardButton(text="🔄 Face Swap", callback_data=IMAGE_FACE_SWAP)
        ],
        [
            InlineKeyboardButton(text="🎬 Generate Video", callback_data=IMAGE_VIDEO_GEN)
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_face_swap_options() -> InlineKeyboardMarkup:
    """Face swap options keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(text="📷 Photo Swap", callback_data="photo_swap"),
            InlineKeyboardButton(text="🎬 Video Swap", callback_data="video_swap")
        ],
        [
            InlineKeyboardButton(text="« Back", callback_data="back_to_actions")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_photo_swap_options() -> InlineKeyboardMarkup:
    """Photo swap options keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(text="« Back", callback_data="back_to_face_swap"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_operation")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_video_swap_options() -> InlineKeyboardMarkup:
    """Video swap options keyboard."""
    keyboard = [
        [
            InlineKeyboardButton(text="🔥 Reels 18+", callback_data="reels_18_plus"),
            InlineKeyboardButton(text="« Back", callback_data="back_to_face_swap")
        ],
        [
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_operation")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def kb_style_selection(page: int = 1) -> InlineKeyboardMarkup:
    """Style selection keyboard with pagination."""
    # Style data - first page styles from the image description
    styles = [
        ("🍑 Succubus Tattoo", "succubus_tattoo"),
        ("😈 Infernal Body Art", "infernal_body_art"),
        ("🖤 Obsidian Skinwear", "obsidian_skinwear"),
        ("🍜 Kikkoman Silk", "kikkoman_silk"),
        ("🖤 Sheer Black Lingerie", "sheer_black_lingerie"),
        ("💦 Face Splash", "face_splash"),
        ("💖 LustFace", "lustface"),
        ("🪡 Silk Restraint", "silk_restraint"),
        ("🌙 Moonlight Seduction", "moonlight_seduction"),
        ("💧 Soaked Tease", "soaked_tease")
    ]
    
    keyboard = []
    
    # Add style buttons in 2 columns x 5 rows
    for i in range(0, len(styles), 2):
        row = []
        for j in range(2):
            if i + j < len(styles):
                style_name, style_id = styles[i + j]
                row.append(InlineKeyboardButton(
                    text=style_name,
                    callback_data=f"{STYLE_SELECT_PREFIX}{style_id}"
                ))
        keyboard.append(row)
    
    # Pagination controls
    pagination_row = []
    if page > 1:
        pagination_row.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=f"{STYLE_PAGE_PREFIX}{page - 1}"
        ))
    pagination_row.append(InlineKeyboardButton(
        text=f"{page}/3",
        callback_data="current_page"
    ))
    if page < 3:
        pagination_row.append(InlineKeyboardButton(
            text="➡️",
            callback_data=f"{STYLE_PAGE_PREFIX}{page + 1}"
        ))
    keyboard.append(pagination_row)
    
    # Additional buttons
    keyboard.append([InlineKeyboardButton(text="⭐ Explore +1500 Options", callback_data="explore_styles")])
    keyboard.append([InlineKeyboardButton(text="BOT LIST 🔥", callback_data="bot_list")])
    keyboard.append([InlineKeyboardButton(text="« Back", callback_data="back_to_actions")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def kb_dynamic_style_selection(page: int = 1) -> InlineKeyboardMarkup:
    """Dynamic style selection keyboard loaded from database."""
    node_repo = NodeRepository()
    nodes = await node_repo.get_all_nodes()
    
    # If no nodes in database, fall back to static styles
    if not nodes:
        return kb_style_selection(page)
    
    keyboard = []
    
    # Add style buttons in 2 columns x 5 rows
    for i in range(0, len(nodes), 2):
        row = []
        for j in range(2):
            if i + j < len(nodes):
                node = nodes[i + j]
                # Use node_name as display text and other_text as callback data
                row.append(InlineKeyboardButton(
                    text=node["node_name"],
                    callback_data=f"{STYLE_SELECT_PREFIX}{node['other_text']}"
                ))
        keyboard.append(row)
    
    # Pagination controls (simplified for now)
    pagination_row = []
    if page > 1:
        pagination_row.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=f"{STYLE_PAGE_PREFIX}{page - 1}"
        ))
    pagination_row.append(InlineKeyboardButton(
        text=f"{page}/1",  # For now, assume single page
        callback_data="current_page"
    ))
    keyboard.append(pagination_row)
    
    # Additional buttons
    keyboard.append([InlineKeyboardButton(text="⭐ Explore +1500 Options", callback_data="explore_styles")])
    keyboard.append([InlineKeyboardButton(text="BOT LIST 🔥", callback_data="bot_list")])
    keyboard.append([InlineKeyboardButton(text="« Back", callback_data="back_to_actions")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

