"""Universal handler for multilingual button matching."""
import logging
from aiogram import Router, F
from aiogram.types import Message
from bot.db.repositories import UserRepository
from bot.languages import get_text, SUPPORTED_LANGUAGES
from bot.handlers import profile, topup, affiliate, free_credit, terms, language

logger = logging.getLogger(__name__)
router = Router()

@router.message()
async def universal_handler(message: Message) -> None:
    """Handle messages by matching translated text across all languages."""
    user_id = message.from_user.id
    text = message.text
    
    # Get user's language preference
    user_repo = UserRepository()
    user = await user_repo.get_user(user_id)
    user_language = user.get("language", "en") if user else "en"
    
    # Check if the message matches any translated button text
    for lang_code in SUPPORTED_LANGUAGES:
        # Check Profile button
        if text == get_text(lang_code, "main_menu.profile"):
            await profile.profile_command(message)
            return
        
        # Check Language button
        if text == get_text(lang_code, "main_menu.language"):
            await language.language_selection(message)
            return
        
        # Check Top up Credit button
        if text == get_text(lang_code, "main_menu.topup"):
            await topup.topup_command(message)
            return
        
        # Check Affiliate money button
        if text == get_text(lang_code, "main_menu.affiliate"):
            await affiliate.affiliate_command(message)
            return
        
        # Check Get Free Credit button
        if text == get_text(lang_code, "main_menu.free_credit"):
            await free_credit.free_credit_command(message)
            return
        
        # Check Terms button
        if text == get_text(lang_code, "main_menu.terms"):
            await terms.terms_command(message)
            return
    
    # If no match found, log it for debugging
    logger.warning(f"Unhandled message: '{text}' from user {user_id}")
