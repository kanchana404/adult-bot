"""Language selection handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot.db.repositories import UserRepository
from bot.languages import SUPPORTED_LANGUAGES, get_language_name, get_language_flag, get_text
from bot.callbacks import BACK_MAIN

logger = logging.getLogger(__name__)
router = Router()

async def language_selection(message: Message) -> None:
    """Show language selection menu."""
    user_id = message.from_user.id
    
    # Get user's current language
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    current_language = user.get("language", "en") if user else "en"
    
    # Create language selection keyboard
    keyboard = []
    languages = list(SUPPORTED_LANGUAGES.items())
    
    # Create rows of 3 buttons each
    for i in range(0, len(languages), 3):
        row = []
        for j in range(3):
            if i + j < len(languages):
                lang_code, lang_info = languages[i + j]
                flag = lang_info["flag"]
                name = lang_info["name"]
                button_text = f"{flag} {name}"
                if lang_code == current_language:
                    button_text += " ✓"
                row.append(InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"lang_{lang_code}"
                ))
        keyboard.append(row)
    
    # Add back button
    keyboard.append([InlineKeyboardButton(
        text=get_text(current_language, "language_selection.back"),
        callback_data=BACK_MAIN
    )])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await message.answer(
        get_text(current_language, "language_selection.title"),
        reply_markup=reply_markup
    )

@router.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery) -> None:
    """Handle language selection."""
    user_id = callback.from_user.id
    language_code = callback.data.replace("lang_", "")
    
    if language_code not in SUPPORTED_LANGUAGES:
        await callback.answer("Invalid language selection!")
        return
    
    # Update user's language preference
    user_repo = UserRepository()
    await user_repo.update_user(user_id, {"language": language_code})
    
    # Get updated language info
    language_name = get_language_name(language_code)
    language_flag = get_language_flag(language_code)
    
    # Send confirmation in the new language
    confirmation_text = get_text(language_code, "language_selection.confirmation").format(
        flag=language_flag,
        name=language_name
    )
    await callback.message.edit_text(confirmation_text)
    
    # Update the main menu with new language
    from bot.keyboards import kb_main_menu
    
    # Create new main menu with updated language
    keyboard = [
        [
            get_text(language_code, "main_menu.profile"),
            get_text(language_code, "main_menu.language"),
            get_text(language_code, "main_menu.topup")
        ],
        [
            get_text(language_code, "main_menu.affiliate"),
            get_text(language_code, "main_menu.free_credit"),
            get_text(language_code, "main_menu.terms")
        ]
    ]
    
    # Send updated main menu
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in keyboard],
        resize_keyboard=True
    )
    
    await callback.message.answer(
        get_text(language_code, "welcome.back"),
        reply_markup=reply_markup
    )
    
    await callback.answer(get_text(language_code, "language_selection.set_to").format(name=language_name))

@router.callback_query(F.data == BACK_MAIN)
async def back_to_main_from_language(callback: CallbackQuery) -> None:
    """Handle back to main menu from language selection."""
    user_id = callback.from_user.id
    
    # Get user's language
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    current_language = user.get("language", "en") if user else "en"
    
    # Send main menu with current language
    from bot.keyboards import kb_main_menu
    
    # Create main menu with current language
    keyboard = [
        [
            get_text(current_language, "main_menu.profile"),
            get_text(current_language, "main_menu.language"),
            get_text(current_language, "main_menu.topup")
        ],
        [
            get_text(current_language, "main_menu.affiliate"),
            get_text(current_language, "main_menu.free_credit"),
            get_text(current_language, "main_menu.terms")
        ]
    ]
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in keyboard],
        resize_keyboard=True
    )
    
    await callback.message.delete()
    await callback.message.answer(
        get_text(current_language, "welcome.back"),
        reply_markup=reply_markup
    )
    
    await callback.answer()
