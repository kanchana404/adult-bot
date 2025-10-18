"""Main entry point for the Telegram bot."""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, PreCheckoutQuery

from bot.config import BOT_TOKEN
from bot.db.mongo import init_mongodb, close_mongodb
from bot.handlers import (
    start, profile, topup, affiliate, 
    free_credit, terms, admin, language, universal
)
from bot.services.payments import PaymentService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    """Handle pre-checkout query - REQUIRED to complete Telegram Stars payment."""
    # Always answer OK to proceed with payment
    await pre_checkout_query.answer(ok=True)
    logger.info(f"Pre-checkout approved for payload: {pre_checkout_query.invoice_payload}")

async def successful_payment_handler(message: Message) -> None:
    """Handle successful payment notification from Telegram."""
    payment = message.successful_payment
    payload = payment.invoice_payload
    telegram_payment_id = payment.telegram_payment_charge_id
    user_id = message.from_user.id
    
    logger.info(f"Payment received: {payload} from user {user_id}")
    
    # Process the payment
    payment_service = PaymentService()
    success = await payment_service.process_successful_payment(
        user_id=user_id,
        payload=payload,
        telegram_payment_id=telegram_payment_id
    )
    
    if success:
        from bot.texts import PAYMENT_CONFIRMED
        # Get payment details
        from bot.db.repositories import PaymentRepository
        payment_repo = PaymentRepository()
        payment_record = await payment_repo.get_payment_by_payload(payload)
        
        if payment_record:
            await message.answer(
                PAYMENT_CONFIRMED.format(
                    stars=payment_record["stars_amount"],
                    tickets=payment_record["tickets_amount"],
                    paid_at=payment_record["paid_at"].strftime("%Y-%m-%d %H:%M:%S") if payment_record.get("paid_at") else "N/A",
                    transaction_id=telegram_payment_id
                )
            )
    else:
        await message.answer(
            "⚠️ There was an issue processing your payment. Please contact support."
        )

async def main() -> None:
    """Main function to run the bot."""
    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Register payment handlers (must be before routers)
    dp.pre_checkout_query.register(pre_checkout_handler)
    dp.message.register(
        successful_payment_handler,
        lambda message: message.successful_payment is not None
    )
    
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


