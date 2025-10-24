"""Telegram utility functions."""
from aiogram import Bot
from bot.config import BOT_TOKEN

async def get_telegram_file_url(bot: Bot, file_id: str) -> str:
    """Get Telegram API URL for a file."""
    try:
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    except Exception as e:
        # Log error and return empty string
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to get file URL for {file_id}: {e}")
        return ""


