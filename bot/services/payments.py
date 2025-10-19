"""Payment service for handling Telegram Stars and other payments."""
import logging
import time
import requests
from typing import Dict, Optional
from datetime import datetime
from decimal import Decimal
from bson import ObjectId
from aiogram import Bot
from aiogram.types import CallbackQuery, LabeledPrice
from bot.config import BOT_TOKEN, CRYPTO_BOT_API_TOKEN, CRYPTO_BOT_API_URL
from bot.db.repositories import PaymentRepository, UserRepository, TransactionRepository, CryptoInvoiceRepository, UnifiedPaymentHistoryRepository
from bot.db.models import Payment, Transaction, CryptoInvoice, UnifiedPaymentHistory
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

# Crypto payment packages configuration
CRYPTO_PACKAGES = [
    {"amount": 5, "currency": "USDT", "tickets": 50, "usd": "5.00", "label": "Starter Pack"},
    {"amount": 10, "currency": "USDT", "tickets": 110, "usd": "10.00", "label": "Basic Pack"},
    {"amount": 25, "currency": "USDT", "tickets": 300, "usd": "25.00", "label": "Popular Pack"},
    {"amount": 50, "currency": "USDT", "tickets": 650, "usd": "50.00", "label": "Premium Pack"},
    {"amount": 100, "currency": "USDT", "tickets": 1400, "usd": "100.00", "label": "Super Pack"},
    {"amount": 0.1, "currency": "TON", "tickets": 50, "usd": "5.00", "label": "TON Starter"},
    {"amount": 0.2, "currency": "TON", "tickets": 110, "usd": "10.00", "label": "TON Basic"},
]

class PaymentService:
    """Service for handling payments."""
    
    def __init__(self):
        self.payment_repo = PaymentRepository()
        self.user_repo = UserRepository()
        self.transaction_repo = TransactionRepository()
        self.crypto_invoice_repo = CryptoInvoiceRepository()
        self.unified_history_repo = UnifiedPaymentHistoryRepository()
    
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
            
            # Credit user tickets (Stars payments only increase tickets, not balance)
            await self.user_repo.increment_tickets(user_id, payment["tickets_amount"])
            
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
            
            # Create unified payment history record
            await self.create_unified_payment_record(
                user_id=user_id,
                username=payment.get("username"),
                payment_type="stars",
                payment_id=payload,
                amount=str(payment["stars_amount"]),
                currency="stars",
                tickets_amount=payment["tickets_amount"],
                usd_amount=payment["usd_amount"],
                status="paid",
                description=f"Telegram Stars Payment - {payment['stars_amount']} stars"
            )
            
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
        """Handle crypto payment - show package selection."""
        from bot.keyboards import kb_crypto_packages
        from bot.texts import CRYPTO_PAYMENT_HEADER
        
        user_id = query.from_user.id
        user = await self.user_repo.get_user(user_id)
        user_language = user.get("language", "en") if user else "en"
        
        await query.answer()
        await query.message.edit_text(
            CRYPTO_PAYMENT_HEADER,
            reply_markup=kb_crypto_packages()
        )
    
    async def create_crypto_invoice(self, query: CallbackQuery, package_index: int) -> None:
        """Create and send crypto invoice."""
        if package_index < 0 or package_index >= len(CRYPTO_PACKAGES):
            await query.answer("Invalid package selected.", show_alert=True)
            return
        
        package = CRYPTO_PACKAGES[package_index]
        user_id = query.from_user.id
        username = query.from_user.username or "unknown"
        
        # Create unique payload
        payload = f"crypto_{user_id}_{int(time.time())}"
        
        try:
            # Create crypto invoice using CryptoBot API
            invoice_data = self.create_crypto_invoice_api(
                amount=package["amount"],
                currency=package["currency"],
                description=f"Get {package['tickets']} tickets for your account"
            )
            
            if not invoice_data:
                await query.answer("Failed to create invoice. Please try again.", show_alert=True)
                return
            
            invoice_id = str(invoice_data.get("invoice_id"))  # Convert to string
            payment_url = invoice_data.get("bot_invoice_url") or invoice_data.get("mini_app_invoice_url")
            
            logger.info(f"Storing invoice in database with ID: {invoice_id} (type: {type(invoice_id)})")
            
            # Store invoice in database
            invoice: CryptoInvoice = {
                "_id": ObjectId(),
                "user_id": user_id,
                "username": username,
                "invoice_id": invoice_id,
                "amount": package["amount"],
                "currency": package["currency"],
                "description": f"Get {package['tickets']} tickets for your account",
                "payment_url": payment_url,
                "status": "active",
                "created_at": datetime.utcnow(),
                "paid_at": None,
                "payload": payload,
                "tickets_amount": package["tickets"],
                "usd_amount": package["usd"]
            }
            await self.crypto_invoice_repo.create_invoice(invoice)
            
            # Send invoice interface
            from bot.keyboards import kb_crypto_invoice_verify
            from bot.texts import CRYPTO_INVOICE_CREATED
            
            await query.answer()
            await query.message.edit_text(
                CRYPTO_INVOICE_CREATED.format(
                    amount=package["amount"],
                    currency=package["currency"],
                    tickets=package["tickets"],
                    invoice_id=invoice_id
                ),
                reply_markup=kb_crypto_invoice_verify(payment_url, invoice_id)
            )
            
            logger.info(f"Created crypto invoice for user {user_id}: {invoice_id}")
            
        except Exception as e:
            logger.error(f"Error creating crypto invoice: {e}")
            await query.answer("Failed to create invoice. Please try again.", show_alert=True)
    
    def create_crypto_invoice_api(self, amount: float, currency: str, description: str) -> Optional[dict]:
        """Create crypto invoice using CryptoBot API."""
        if not CRYPTO_BOT_API_TOKEN:
            logger.error("CRYPTO_BOT_API_TOKEN not configured")
            return None
        
        url = f"{CRYPTO_BOT_API_URL}/createInvoice"
        
        headers = {
            "Crypto-Pay-API-Token": CRYPTO_BOT_API_TOKEN
        }
        
        payload = {
            "asset": currency,
            "amount": str(amount),
            "description": description,
            "paid_btn_name": "callback",
            "paid_btn_url": "https://t.me/your_bot"  # You can customize this
        }
        
        try:
            logger.info(f"Creating crypto invoice: {amount} {currency}")
            logger.info(f"API URL: {url}")
            logger.info(f"API Token: {CRYPTO_BOT_API_TOKEN[:10]}..." if CRYPTO_BOT_API_TOKEN else "No token")
            logger.info(f"Payload: {payload}")
            
            response = requests.post(url, headers=headers, json=payload)
            logger.info(f"API Response Status: {response.status_code}")
            
            result = response.json()
            logger.info(f"API Response: {result}")
            
            if result.get("ok"):
                invoice_data = result.get("result")
                logger.info(f"Created invoice successfully: {invoice_data}")
                return invoice_data
            else:
                logger.error(f"CryptoBot API error: {result}")
                return None
        except Exception as e:
            logger.error(f"Error calling CryptoBot API: {e}")
            return None
    
    def get_crypto_invoice_status_api(self, invoice_id: str) -> Optional[dict]:
        """Check crypto invoice status using CryptoBot API."""
        if not CRYPTO_BOT_API_TOKEN:
            logger.error("CRYPTO_BOT_API_TOKEN not configured")
            return None
        
        url = f"{CRYPTO_BOT_API_URL}/getInvoices"
        
        headers = {
            "Crypto-Pay-API-Token": CRYPTO_BOT_API_TOKEN
        }
        
        params = {
            "invoice_ids": invoice_id
        }
        
        try:
            logger.info(f"Checking crypto invoice status for ID: {invoice_id}")
            logger.info(f"API URL: {url}")
            logger.info(f"API Token: {CRYPTO_BOT_API_TOKEN[:10]}..." if CRYPTO_BOT_API_TOKEN else "No token")
            
            response = requests.get(url, headers=headers, params=params)
            logger.info(f"API Response Status: {response.status_code}")
            
            result = response.json()
            logger.info(f"API Response: {result}")
            
            if result.get("ok") and result.get("result", {}).get("items"):
                invoice_data = result["result"]["items"][0]
                logger.info(f"Found invoice data: {invoice_data}")
                return invoice_data
            else:
                logger.warning(f"API returned error or no items: {result}")
                return None
        except Exception as e:
            logger.error(f"Error checking crypto invoice status: {e}")
            return None
    
    async def check_crypto_invoice_status(self, query: CallbackQuery, invoice_id: str) -> None:
        """Check crypto invoice payment status."""
        user_id = query.from_user.id
        
        logger.info(f"Checking crypto invoice status for user {user_id}, invoice {invoice_id}")
        
        # Check invoice in database
        logger.info(f"Looking for invoice in database with ID: {invoice_id} (type: {type(invoice_id)})")
        invoice = await self.crypto_invoice_repo.get_invoice_by_id(invoice_id)
        
        if not invoice:
            logger.warning(f"Invoice not found in database: {invoice_id}")
            # Let's also try to see what invoices exist for this user
            user_invoices = await self.crypto_invoice_repo.get_user_invoices(user_id, limit=5)
            logger.info(f"User {user_id} has {len(user_invoices)} invoices:")
            for inv in user_invoices:
                logger.info(f"  - Invoice ID: {inv['invoice_id']} (type: {type(inv['invoice_id'])})")
            await query.answer("Invoice not found.", show_alert=True)
            return
        
        if invoice["user_id"] != user_id:
            logger.warning(f"Invoice {invoice_id} doesn't belong to user {user_id}")
            await query.answer("This invoice doesn't belong to you.", show_alert=True)
            return
        
        # Show checking message
        await query.answer("Checking payment status...")
        await query.message.edit_text("🔍 Checking payment status...")
        
        # Check with CryptoBot API
        invoice_data = self.get_crypto_invoice_status_api(invoice_id)
        
        if not invoice_data:
            logger.error(f"Could not retrieve invoice status from API for {invoice_id}")
            await query.message.edit_text(
                "❌ Could not retrieve invoice status.\n\n"
                "This might be due to:\n"
                "• API configuration issue\n"
                "• Network connectivity problem\n"
                "• Invoice not found in CryptoBot system\n\n"
                "Please try again later or contact support."
            )
            return
        
        status = invoice_data.get("status")
        
        if status == "paid":
            # Process successful payment FIRST, then update status
            success = await self.process_successful_crypto_payment(
                user_id=user_id,
                invoice_id=invoice_id,
                invoice_data=invoice_data
            )
            
            # Only update database status after successful processing
            if success:
                await self.crypto_invoice_repo.update_invoice_status(invoice_id, status)
                
                from bot.texts import CRYPTO_INVOICE_CONFIRMED
                await query.answer()
                await query.message.edit_text(
                    CRYPTO_INVOICE_CONFIRMED.format(
                        amount=invoice["amount"],
                        currency=invoice["currency"],
                        tickets=invoice["tickets_amount"],
                        paid_at=invoice_data.get("paid_at", "N/A"),
                        invoice_id=invoice_id
                    )
                )
            else:
                await query.answer("Payment confirmed but there was an issue crediting your account.", show_alert=True)
        elif status == "active":
            # Update database for active status
            await self.crypto_invoice_repo.update_invoice_status(invoice_id, status)
            
            from bot.keyboards import kb_crypto_invoice_verify
            from bot.texts import CRYPTO_INVOICE_PENDING
            
            await query.answer("Payment still pending. Please complete the payment first.", show_alert=False)
            await query.message.edit_text(
                CRYPTO_INVOICE_PENDING.format(
                    amount=invoice["amount"],
                    currency=invoice["currency"],
                    tickets=invoice["tickets_amount"],
                    status=status
                ),
                reply_markup=kb_crypto_invoice_verify(invoice["payment_url"], invoice_id)
            )
        elif status == "expired":
            # Update database for expired status
            await self.crypto_invoice_repo.update_invoice_status(invoice_id, status)
            
            from bot.texts import CRYPTO_INVOICE_EXPIRED
            await query.answer()
            await query.message.edit_text(CRYPTO_INVOICE_EXPIRED)
        else:
            # Update database for other statuses
            await self.crypto_invoice_repo.update_invoice_status(invoice_id, status)
            
            from bot.keyboards import kb_crypto_invoice_verify
            await query.answer(f"Invoice status: {status}. Check again in a moment.", show_alert=False)
            await query.message.edit_text(
                f"ℹ️ Invoice Status: {status}\n\nCheck again in a moment.",
                reply_markup=kb_crypto_invoice_verify(invoice["payment_url"], invoice_id)
            )
    
    async def process_successful_crypto_payment(
        self, 
        user_id: int, 
        invoice_id: str, 
        invoice_data: dict
    ) -> bool:
        """Process successful crypto payment - update database and credit user."""
        try:
            logger.info(f"Processing successful crypto payment for user {user_id}, invoice {invoice_id}")
            
            # Get invoice record
            invoice = await self.crypto_invoice_repo.get_invoice_by_id(invoice_id)
            
            if not invoice:
                logger.error(f"Crypto invoice not found: {invoice_id}")
                return False
            
            logger.info(f"Found invoice: {invoice}")
            
            if invoice["status"] == "paid":
                logger.warning(f"Crypto invoice already processed: {invoice_id}")
                return True
            
            # Get current user data
            current_user = await self.user_repo.get_user(user_id)
            if not current_user:
                logger.error(f"User not found: {user_id}")
                return False
            
            logger.info(f"Current user data: {current_user}")
            logger.info(f"Crediting {invoice['tickets_amount']} tickets (no balance increase)")
            
            # Credit user tickets (Crypto payments only increase tickets, not balance)
            await self.user_repo.increment_tickets(user_id, invoice["tickets_amount"])
            logger.info(f"Credited {invoice['tickets_amount']} tickets to user {user_id}")
            
            # Create transaction record
            transaction: Transaction = {
                "_id": ObjectId(),
                "user_id": user_id,
                "type": "payment",
                "amount_tickets": invoice["tickets_amount"],
                "amount_usd": invoice["usd_amount"],
                "meta": {
                    "payment_method": "crypto",
                    "currency": invoice["currency"],
                    "amount": invoice["amount"],
                    "invoice_id": invoice_id,
                    "payload": invoice["payload"]
                },
                "created_at": datetime.utcnow()
            }
            await self.transaction_repo.create_transaction(transaction)
            logger.info(f"Created transaction record for user {user_id}")
            
            # Create unified payment history record
            await self.create_unified_payment_record(
                user_id=user_id,
                username=invoice.get("username"),
                payment_type="crypto",
                payment_id=invoice_id,
                amount=str(invoice["amount"]),
                currency=invoice["currency"],
                tickets_amount=invoice["tickets_amount"],
                usd_amount=invoice["usd_amount"],
                status="paid",
                description=f"Crypto Payment - {invoice['amount']} {invoice['currency']}"
            )
            
            # Verify the changes
            updated_user = await self.user_repo.get_user(user_id)
            logger.info(f"Updated user data: {updated_user}")
            
            logger.info(f"Successfully processed crypto payment {invoice_id} for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing crypto payment: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    async def get_crypto_payment_history(self, user_id: int) -> str:
        """Get user's crypto payment history as formatted text."""
        from bot.texts import CRYPTO_HISTORY_HEADER, CRYPTO_HISTORY_EMPTY
        
        invoices = await self.crypto_invoice_repo.get_user_invoices(user_id)
        
        if not invoices:
            return CRYPTO_HISTORY_EMPTY
        
        text = CRYPTO_HISTORY_HEADER
        for invoice in invoices:
            emoji = "✅" if invoice["status"] == "paid" else "⏳" if invoice["status"] == "active" else "❌"
            text += f"\n{emoji} {invoice['amount']} {invoice['currency']} → {invoice['tickets_amount']} 🎟 Tickets"
            text += f"\n   Status: {invoice['status'].upper()}"
            text += f"\n   Created: {invoice['created_at'].strftime('%Y-%m-%d %H:%M')}"
            if invoice.get("paid_at"):
                text += f"\n   Paid: {invoice['paid_at'].strftime('%Y-%m-%d %H:%M')}"
            text += "\n"
        
        return text
    
    async def handle_paypal_payment(self, query: CallbackQuery) -> None:
        """Handle PayPal payment."""
        await query.answer("PayPal payment coming soon.")
        await query.message.edit_text("PayPal payment coming soon.")
    
    async def create_unified_payment_record(
        self, 
        user_id: int, 
        username: Optional[str], 
        payment_type: str, 
        payment_id: str, 
        amount: str, 
        currency: str, 
        tickets_amount: int, 
        usd_amount: str, 
        status: str, 
        description: str
    ) -> None:
        """Create a unified payment history record."""
        payment_record: UnifiedPaymentHistory = {
            "_id": ObjectId(),
            "user_id": user_id,
            "username": username,
            "payment_type": payment_type,
            "payment_id": payment_id,
            "amount": amount,
            "currency": currency,
            "tickets_amount": tickets_amount,
            "usd_amount": usd_amount,
            "status": status,
            "created_at": datetime.utcnow(),
            "paid_at": None,
            "description": description
        }
        
        await self.unified_history_repo.create_payment_record(payment_record)
        logger.info(f"Created unified payment record: {payment_type} - {payment_id}")
    
    async def migrate_existing_payments(self, user_id: int) -> None:
        """Migrate existing payments to unified payment history."""
        try:
            # Check if user already has unified payment records
            existing_unified = await self.unified_history_repo.get_user_payment_history(user_id, 1, 1)
            if existing_unified[0]:  # If there are already unified records, skip migration
                return
            
            logger.info(f"Migrating existing payments for user {user_id}")
            
            # Migrate Stars payments
            stars_payments = await self.payment_repo.get_user_payments(user_id, limit=100)
            for payment in stars_payments:
                await self.create_unified_payment_record(
                    user_id=user_id,
                    username=payment.get("username"),
                    payment_type="stars",
                    payment_id=payment["payload"],
                    amount=str(payment["stars_amount"]),
                    currency="stars",
                    tickets_amount=payment["tickets_amount"],
                    usd_amount=payment["usd_amount"],
                    status=payment["status"],
                    description=f"Telegram Stars Payment - {payment['stars_amount']} stars"
                )
            
            # Migrate Crypto payments
            crypto_invoices = await self.crypto_invoice_repo.get_user_invoices(user_id, limit=100)
            for invoice in crypto_invoices:
                await self.create_unified_payment_record(
                    user_id=user_id,
                    username=invoice.get("username"),
                    payment_type="crypto",
                    payment_id=invoice["invoice_id"],
                    amount=str(invoice["amount"]),
                    currency=invoice["currency"],
                    tickets_amount=invoice["tickets_amount"],
                    usd_amount=invoice["usd_amount"],
                    status=invoice["status"],
                    description=f"Crypto Payment - {invoice['amount']} {invoice['currency']}"
                )
            
            logger.info(f"Migration completed for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error migrating payments for user {user_id}: {e}")

    async def get_unified_payment_history(self, user_id: int, page: int = 1) -> tuple[str, bool, bool]:
        """Get unified payment history with pagination."""
        from bot.texts import UNIFIED_PAYMENT_HISTORY_HEADER, UNIFIED_PAYMENT_HISTORY_EMPTY
        
        # Migrate existing payments first
        await self.migrate_existing_payments(user_id)
        
        payments, total_count = await self.unified_history_repo.get_user_payment_history(user_id, page, 3)
        
        if not payments:
            return UNIFIED_PAYMENT_HISTORY_EMPTY, False, False
        
        text = UNIFIED_PAYMENT_HISTORY_HEADER.format(page=page, total=total_count)
        
        for payment in payments:
            # Status emoji
            if payment["status"] == "paid":
                emoji = "✅"
            elif payment["status"] in ["pending", "active"]:
                emoji = "⏳"
            else:
                emoji = "❌"
            
            # Payment type emoji
            type_emoji = "⭐" if payment["payment_type"] == "stars" else "₿"
            
            text += f"\n{emoji} {type_emoji} {payment['amount']} {payment['currency']} → {payment['tickets_amount']} 🎟"
            text += f"\n   Status: {payment['status'].upper()}"
            text += f"\n   Created: {payment['created_at'].strftime('%Y-%m-%d %H:%M')}"
            if payment.get("paid_at"):
                text += f"\n   Paid: {payment['paid_at'].strftime('%Y-%m-%d %H:%M')}"
            text += "\n"
        
        # Pagination info
        has_previous = page > 1
        has_next = (page * 3) < total_count
        
        return text, has_previous, has_next


