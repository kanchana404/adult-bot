"""Main entry point for the Telegram bot."""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.db.mongo import init_mongodb, close_mongodb
from bot.handlers import (
    start, profile, topup, affiliate, 
    free_credit, terms, admin, language, universal
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main() -> None:
    """Main function to run the bot."""
    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(language.router)
    dp.include_router(profile.router)  # For callback handlers
    dp.include_router(topup.router)    # For callback handlers
    dp.include_router(affiliate.router) # For callback handlers
    dp.include_router(free_credit.router) # For callback handlers
    dp.include_router(terms.router)    # For callback handlers
    dp.include_router(universal.router)  # Universal handler must be last
    
    try:
        # Initialize MongoDB
        await init_mongodb()
        logger.info("MongoDB initialized successfully")
        
        # Start polling
        logger.info("Starting bot polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        # Close MongoDB connection
        await close_mongodb()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise


