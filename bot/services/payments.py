"""Payment service for handling Telegram Stars and other payments."""
import logging
import time
from typing import Dict, Optional
from datetime import datetime
from decimal import Decimal
from bson import ObjectId
from aiogram import Bot
from aiogram.types import CallbackQuery, LabeledPrice
from bot.config import BOT_TOKEN
from bot.db.repositories import PaymentRepository, UserRepository, TransactionRepository
from bot.db.models import Payment, Transaction
from bot.languages import get_text

logger = logging.getLogger(__name__)

# Payment packages configuration
PAYMENT_PACKAGES = [
    {"stars": 1, "tickets": 1, "usd": "0.01", "label": "🧪 Test Pack (1 Star)"},
    {"stars": 100, "tickets": 10, "usd": "1.00", "label": "Starter Pack"},
    {"stars": 250, "tickets": 30, "usd": "2.50", "label": "Basic Pack"},
    {"stars": 500, "tickets": 65, "usd": "5.00", "label": "Popular Pack"},
    {"stars": 1000, "tickets": 140, "usd": "10.00", "label": "Premium Pack"},
    {"stars": 2500, "tickets": 375, "usd": "25.00", "label": "Super Pack"},
    {"stars": 5000, "tickets": 800, "usd": "50.00", "label": "Mega Pack"},
]

class PaymentService:
    """Service for handling payments."""
    
    def __init__(self):
        self.payment_repo = PaymentRepository()
        self.user_repo = UserRepository()
        self.transaction_repo = TransactionRepository()
    
    async def handle_telegram_star_payment(self, query: CallbackQuery) -> None:
        """Handle Telegram Stars payment - show package selection."""
        from bot.keyboards import kb_star_packages
        from bot.texts import STARS_PAYMENT_HEADER
        
        user_id = query.from_user.id
        user = await self.user_repo.get_user(user_id)
        user_language = user.get("language", "en") if user else "en"
        
        await query.answer()
        await query.message.edit_text(
            STARS_PAYMENT_HEADER,
            reply_markup=kb_star_packages()
        )
    
    async def create_star_invoice(self, query: CallbackQuery, package_index: int) -> None:
        """Create and send Telegram Stars invoice."""
        if package_index < 0 or package_index >= len(PAYMENT_PACKAGES):
            await query.answer("Invalid package selected.", show_alert=True)
            return
        
        package = PAYMENT_PACKAGES[package_index]
        user_id = query.from_user.id
        username = query.from_user.username or "unknown"
        
        # Create unique payload
        payload = f"stars_{user_id}_{int(time.time())}"
        
        try:
            # Create invoice link
            bot = Bot(token=BOT_TOKEN)
            invoice_url = await self.create_invoice_link(
                bot=bot,
                title=package["label"],
                description=f"Get {package['tickets']} tickets for your account",
                stars_amount=package["stars"],
                payload=payload
            )
            
            if not invoice_url:
                await query.answer("Failed to create payment link. Please try again.", show_alert=True)
                return
            
            # Store payment in database
            payment: Payment = {
                "_id": ObjectId(),
                "user_id": user_id,
                "username": username,
                "payload": payload,
                "stars_amount": package["stars"],
                "tickets_amount": package["tickets"],
                "usd_amount": package["usd"],
                "payment_url": invoice_url,
                "status": "pending",
                "created_at": datetime.utcnow(),
                "paid_at": None,
                "telegram_payment_id": None
            }
            await self.payment_repo.create_payment(payment)
            
            # Send payment interface
            from bot.keyboards import kb_payment_verify
            from bot.texts import PAYMENT_INSTRUCTIONS
            
            await query.answer()
            await query.message.edit_text(
                PAYMENT_INSTRUCTIONS.format(
                    package=package["label"],
                    stars=package["stars"],
                    tickets=package["tickets"],
                    usd=package["usd"]
                ),
                reply_markup=kb_payment_verify(invoice_url, payload)
            )
            
            logger.info(f"Created payment for user {user_id}: {payload}")
            
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            await query.answer("Failed to create payment. Please try again.", show_alert=True)
    
    async def create_invoice_link(
        self, 
        bot: Bot,
        title: str,
        description: str,
        stars_amount: int,
        payload: str
    ) -> Optional[str]:
        """Create Telegram Stars invoice link."""
        try:
            # Create invoice link using Bot API
            invoice_link = await bot.create_invoice_link(
                title=title,
                description=description,
                payload=payload,
                currency="XTR",  # Telegram Stars currency
                prices=[LabeledPrice(label=title, amount=stars_amount)]
            )
            return invoice_link
        except Exception as e:
            logger.error(f"Error creating invoice link: {e}")
            return None
    
    async def verify_payment(self, query: CallbackQuery, payload: str) -> None:
        """Verify if payment has been completed."""
        user_id = query.from_user.id
        
        # Check payment status in database
        payment = await self.payment_repo.get_payment_by_payload(payload)
        
        if not payment:
            await query.answer("Payment record not found.", show_alert=True)
            return
        
        if payment["user_id"] != user_id:
            await query.answer("This payment doesn't belong to you.", show_alert=True)
            return
        
        if payment["status"] == "paid":
            # Payment already completed
            from bot.texts import PAYMENT_CONFIRMED
            await query.answer()
            await query.message.edit_text(
                PAYMENT_CONFIRMED.format(
                    stars=payment["stars_amount"],
                    tickets=payment["tickets_amount"],
                    paid_at=payment["paid_at"].strftime("%Y-%m-%d %H:%M:%S") if payment["paid_at"] else "N/A",
                    transaction_id=payment["telegram_payment_id"] or "N/A"
                )
            )
        else:
            # Payment still pending
            from bot.keyboards import kb_payment_verify
            from bot.texts import PAYMENT_PENDING
            
            await query.answer("Payment not detected yet. Please complete the payment first.", show_alert=False)
            await query.message.edit_text(
                PAYMENT_PENDING.format(
                    stars=payment["stars_amount"],
                    tickets=payment["tickets_amount"]
                ),
                reply_markup=kb_payment_verify(payment["payment_url"], payload)
            )
    
    async def process_successful_payment(
        self, 
        user_id: int, 
        payload: str, 
        telegram_payment_id: str
    ) -> bool:
        """Process successful payment - update database and credit user."""
        try:
            # Get payment record
            payment = await self.payment_repo.get_payment_by_payload(payload)
            
            if not payment:
                logger.error(f"Payment not found for payload: {payload}")
                return False
            
            if payment["status"] == "paid":
                logger.warning(f"Payment already processed: {payload}")
                return True
            
            # Update payment status
            await self.payment_repo.update_payment_status(payload, telegram_payment_id)
            
            # Credit user tickets
            await self.user_repo.increment_tickets(user_id, payment["tickets_amount"])
            
            # Update user balance
            current_user = await self.user_repo.get_user(user_id)
            if current_user:
                current_balance = Decimal(current_user["balance_usd"])
                new_balance = current_balance + Decimal(payment["usd_amount"])
                await self.user_repo.update_user(user_id, {"balance_usd": str(new_balance)})
            
            # Create transaction record
            transaction: Transaction = {
                "_id": ObjectId(),
                "user_id": user_id,
                "type": "payment",
                "amount_tickets": payment["tickets_amount"],
                "amount_usd": payment["usd_amount"],
                "meta": {
                    "payment_method": "telegram_stars",
                    "stars_amount": payment["stars_amount"],
                    "telegram_payment_id": telegram_payment_id,
                    "payload": payload
                },
                "created_at": datetime.utcnow()
            }
            await self.transaction_repo.create_transaction(transaction)
            
            logger.info(f"Successfully processed payment {payload} for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return False
    
    async def get_payment_history(self, user_id: int) -> str:
        """Get user's payment history as formatted text."""
        from bot.texts import PAYMENT_HISTORY_HEADER, PAYMENT_HISTORY_EMPTY
        
        payments = await self.payment_repo.get_user_payments(user_id)
        
        if not payments:
            return PAYMENT_HISTORY_EMPTY
        
        text = PAYMENT_HISTORY_HEADER
        for payment in payments:
            emoji = "✅" if payment["status"] == "paid" else "⏳"
            text += f"\n{emoji} {payment['stars_amount']} ⭐ Stars → {payment['tickets_amount']} 🎟 Tickets"
            text += f"\n   Status: {payment['status'].upper()}"
            text += f"\n   Created: {payment['created_at'].strftime('%Y-%m-%d %H:%M')}"
            if payment.get("paid_at"):
                text += f"\n   Paid: {payment['paid_at'].strftime('%Y-%m-%d %H:%M')}"
            text += "\n"
        
        return text
    
    async def handle_crypto_payment(self, query: CallbackQuery) -> None:
        """Handle crypto payment."""
        await query.answer("Crypto payment coming soon.")
        await query.message.edit_text("Crypto payment coming soon.")
    
    async def handle_paypal_payment(self, query: CallbackQuery) -> None:
        """Handle PayPal payment."""
        await query.answer("PayPal payment coming soon.")
        await query.message.edit_text("PayPal payment coming soon.")


