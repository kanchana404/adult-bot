"""Payment service stubs."""
import logging
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)

class PaymentService:
    """Service for handling payments (stubs for now)."""
    
    async def handle_telegram_star_payment(self, query: CallbackQuery) -> None:
        """Handle Telegram Stars payment."""
        await query.answer("Telegram Stars payment coming soon.")
        await query.edit_message_text("Telegram Stars payment coming soon.")
    
    async def handle_crypto_payment(self, query: CallbackQuery) -> None:
        """Handle crypto payment."""
        await query.answer("Crypto payment coming soon.")
        await query.edit_message_text("Crypto payment coming soon.")
    
    async def handle_paypal_payment(self, query: CallbackQuery) -> None:
        """Handle PayPal payment."""
        await query.answer("PayPal payment coming soon.")
        await query.edit_message_text("PayPal payment coming soon.")


