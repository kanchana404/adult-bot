import requests
import json
import time
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Configuration
BOT_TOKEN = "8247161134:AAGqiDo9rkfd5050pTEu-H21rYvm6Lvmr-o"  # Your Telegram bot
SEND_BOT_USERNAME = "send"  # @send bot username

# @send API Configuration
CRYPTO_BOT_API_TOKEN = "27308:AAHJWxQDyJxdC2WDpKOWLAIWvAuqGcwJu7D"  # CryptoTestnetBot API token
CRYPTO_BOT_API_URL = "https://testnet-pay.crypt.bot/api"  # Testnet
# For production use: https://pay.crypt.bot/api

# Initialize Database
def init_db():
    """Create database to track crypto payments"""
    conn = sqlite3.connect('crypto_payments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS invoices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  username TEXT,
                  invoice_id TEXT UNIQUE,
                  amount REAL,
                  currency TEXT,
                  description TEXT,
                  payment_url TEXT,
                  status TEXT DEFAULT 'pending',
                  created_at TEXT,
                  paid_at TEXT,
                  payload TEXT)''')
    conn.commit()
    conn.close()

def create_invoice_record(user_id, username, invoice_id, amount, currency, description, payment_url, payload):
    """Store invoice in database"""
    conn = sqlite3.connect('crypto_payments.db')
    c = conn.cursor()
    c.execute('''INSERT INTO invoices 
                 (user_id, username, invoice_id, amount, currency, description, payment_url, created_at, status, payload)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_id, username, invoice_id, amount, currency, description, payment_url,
               datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'pending', payload))
    conn.commit()
    conn.close()

def update_invoice_status(invoice_id, status):
    """Update invoice payment status"""
    conn = sqlite3.connect('crypto_payments.db')
    c = conn.cursor()
    paid_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == 'paid' else None
    c.execute('''UPDATE invoices 
                 SET status = ?, paid_at = ?
                 WHERE invoice_id = ?''',
              (status, paid_at, invoice_id))
    conn.commit()
    conn.close()

def check_invoice_status(user_id, invoice_id):
    """Check invoice status from database"""
    conn = sqlite3.connect('crypto_payments.db')
    c = conn.cursor()
    c.execute('''SELECT status, paid_at, amount, currency FROM invoices 
                 WHERE user_id = ? AND invoice_id = ?''', (user_id, invoice_id))
    result = c.fetchone()
    conn.close()
    return result

def get_user_invoices(user_id):
    """Get all invoices for a user"""
    conn = sqlite3.connect('crypto_payments.db')
    c = conn.cursor()
    c.execute('''SELECT invoice_id, amount, currency, status, created_at, paid_at 
                 FROM invoices WHERE user_id = ?
                 ORDER BY created_at DESC LIMIT 10''', (user_id,))
    results = c.fetchall()
    conn.close()
    return results

# CryptoBot API Functions
def create_crypto_invoice(amount, currency="USDT", description="Payment"):
    """
    Create invoice using CryptoBot API
    
    Args:
        amount: Amount in selected currency (e.g., 5 for $5)
        currency: Currency code (USDT, TON, BTC, ETH, etc.)
        description: Invoice description
    
    Returns:
        Invoice data or None
    """
    url = f"{CRYPTO_BOT_API_URL}/createInvoice"
    
    headers = {
        "Crypto-Pay-API-Token": CRYPTO_BOT_API_TOKEN
    }
    
    payload = {
        "asset": currency,
        "amount": str(amount),
        "description": description,
        "paid_btn_name": "callback",  # Show button after payment
        "paid_btn_url": "https://t.me/your_bot"  # Your bot link
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if result.get("ok"):
            return result.get("result")
        else:
            print(f"❌ Error: {result}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def get_crypto_invoice_status(invoice_id):
    """
    Check invoice status using CryptoBot API
    
    Args:
        invoice_id: Invoice ID to check
    
    Returns:
        Invoice data with status
    """
    url = f"{CRYPTO_BOT_API_URL}/getInvoices"
    
    headers = {
        "Crypto-Pay-API-Token": CRYPTO_BOT_API_TOKEN
    }
    
    params = {
        "invoice_ids": invoice_id
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        if result.get("ok") and result.get("result", {}).get("items"):
            return result["result"]["items"][0]
        return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

# Bot Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    keyboard = [
        [InlineKeyboardButton("💵 Create $5 Invoice", callback_data="create_5usd")],
        [InlineKeyboardButton("💰 Create Custom Invoice", callback_data="create_custom")],
        [InlineKeyboardButton("📊 My Invoices", callback_data="my_invoices")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔐 Crypto Payment Bot\n\n"
        "Create and manage cryptocurrency payment invoices.\n"
        "Powered by @send\n\n"
        "Choose an option below:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username or "unknown"
    
    if query.data == "create_5usd":
        # Create $5 USDT invoice
        await query.edit_message_text("⏳ Creating $5 invoice...")
        
        invoice = create_crypto_invoice(
            amount=5,
            currency="USDT",
            description="$5 Payment"
        )
        
        if invoice:
            invoice_id = invoice.get("invoice_id")
            payment_url = invoice.get("bot_invoice_url") or invoice.get("mini_app_invoice_url")
            
            # Store in database
            create_invoice_record(
                user_id, username, invoice_id, 5, "USDT",
                "$5 Payment", payment_url, f"payment_{user_id}_{int(time.time())}"
            )
            
            # Send invoice with verification button
            keyboard = [
                [InlineKeyboardButton("💳 Pay Invoice", url=payment_url)],
                [InlineKeyboardButton("✅ Check Payment Status", callback_data=f"check_{invoice_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "💵 Invoice Created!\n\n"
                f"💰 Amount: $5 USDT\n"
                f"🔖 Invoice ID: {invoice_id}\n\n"
                "1️⃣ Click 'Pay Invoice' to pay via @send\n"
                "2️⃣ Complete payment\n"
                "3️⃣ Click 'Check Payment Status' to verify\n\n"
                f"⏰ Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text(
                "❌ Failed to create invoice.\n\n"
                "Please make sure:\n"
                "• CryptoBot API token is set\n"
                "• API is accessible\n"
                "• Check error logs"
            )
    
    elif query.data == "create_custom":
        await query.edit_message_text(
            "💰 Custom Invoice Creation\n\n"
            "Send amount in format:\n"
            "/invoice <amount> <currency>\n\n"
            "Examples:\n"
            "• /invoice 10 USDT\n"
            "• /invoice 0.1 TON\n"
            "• /invoice 0.0001 BTC\n\n"
            "Supported: USDT, TON, BTC, ETH, LTC, BNB, TRX, USDC"
        )
    
    elif query.data.startswith("check_"):
        # Extract invoice_id
        invoice_id = query.data.replace("check_", "")
        
        await query.edit_message_text("🔍 Checking payment status...")
        
        # Check with CryptoBot API
        invoice_data = get_crypto_invoice_status(invoice_id)
        
        if invoice_data:
            status = invoice_data.get("status")
            
            # Update database
            update_invoice_status(invoice_id, status)
            
            if status == "paid":
                await query.edit_message_text(
                    "✅ PAYMENT CONFIRMED!\n\n"
                    f"💰 Amount: {invoice_data.get('amount')} {invoice_data.get('asset')}\n"
                    f"🔖 Invoice ID: {invoice_id}\n"
                    f"📅 Paid at: {invoice_data.get('paid_at')}\n\n"
                    "🎉 Thank you for your payment!"
                )
            elif status == "active":
                keyboard = [
                    [InlineKeyboardButton("🔄 Check Again", callback_data=f"check_{invoice_id}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    "⏳ Payment Pending\n\n"
                    f"Invoice is still active and awaiting payment.\n\n"
                    f"Status: {status}\n"
                    "Please complete the payment and check again.",
                    reply_markup=reply_markup
                )
            elif status == "expired":
                await query.edit_message_text(
                    "⏰ Invoice Expired\n\n"
                    "This invoice has expired.\n"
                    "Please create a new invoice."
                )
            else:
                keyboard = [
                    [InlineKeyboardButton("🔄 Check Again", callback_data=f"check_{invoice_id}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    f"ℹ️ Invoice Status: {status}\n\n"
                    "Check again in a moment.",
                    reply_markup=reply_markup
                )
        else:
            await query.edit_message_text("❌ Could not retrieve invoice status.")
    
    elif query.data == "my_invoices":
        invoices = get_user_invoices(user_id)
        
        if invoices:
            text = "📊 Your Recent Invoices:\n\n"
            for inv_id, amount, currency, status, created, paid in invoices:
                emoji = "✅" if status == "paid" else "⏳" if status == "active" else "❌"
                text += f"{emoji} {amount} {currency} - {status.upper()}\n"
                text += f"   ID: {inv_id[:20]}...\n"
                text += f"   Created: {created}\n"
                if paid:
                    text += f"   Paid: {paid}\n"
                text += "\n"
        else:
            text = "No invoices found."
        
        await query.edit_message_text(text)

async def create_custom_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /invoice command for custom amounts"""
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text(
                "Usage: /invoice <amount> <currency>\n"
                "Example: /invoice 10 USDT"
            )
            return
        
        amount = float(args[0])
        currency = args[1].upper()
        
        user_id = update.effective_user.id
        username = update.effective_user.username or "unknown"
        
        await update.message.reply_text("⏳ Creating invoice...")
        
        invoice = create_crypto_invoice(
            amount=amount,
            currency=currency,
            description=f"{amount} {currency} Payment"
        )
        
        if invoice:
            invoice_id = invoice.get("invoice_id")
            payment_url = invoice.get("bot_invoice_url") or invoice.get("mini_app_invoice_url")
            
            create_invoice_record(
                user_id, username, invoice_id, amount, currency,
                f"{amount} {currency} Payment", payment_url,
                f"payment_{user_id}_{int(time.time())}"
            )
            
            keyboard = [
                [InlineKeyboardButton("💳 Pay Invoice", url=payment_url)],
                [InlineKeyboardButton("✅ Check Status", callback_data=f"check_{invoice_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"💵 Invoice Created!\n\n"
                f"💰 Amount: {amount} {currency}\n"
                f"🔖 Invoice ID: {invoice_id}\n\n"
                "Click 'Pay Invoice' to complete payment.",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("❌ Failed to create invoice.")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    """Start the bot"""
    print("🚀 Starting Crypto Payment Bot...")
    print(f"Bot Token: {BOT_TOKEN[:20]}...")
    print(f"API URL: {CRYPTO_BOT_API_URL}")
    
    # Initialize database
    init_db()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("invoice", create_custom_invoice))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print("\n⚠️  IMPORTANT: Set your CRYPTO_BOT_API_TOKEN to enable payments!")
    print("Get it from: @CryptoTestnetBot (for testing) or @CryptoBot (production)")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()