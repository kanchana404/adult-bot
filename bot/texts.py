"""Text templates for the bot messages."""

# Profile text template
PROFILE_TEXT = """💼 Account ID: {account_id}

💵Balance: ${balance}
💎You have {tickets} tickets, of which {vip}🏆 VIP spins are not
🎰Lucky spins: {lucky}

You have earned {ref_tickets:.2f} tickets from referrals

You have invited {invited} people"""

# Top up header template
TOPUP_HEADER = """🎟 Top up Credit
TOP UP CREDIT $ PAYMENT OPTION

💼 Account ID: {account_id}
💵 Balance: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Lucky spins: {lucky}

⚙️ Usage Details:
 • 1 🎟 = 1 AI-generated image 🖼
 • 2 🎟 = 1 Video V1 generation 🎬
 • 4 🎟 = 1 Video V2 generation 🎬✨
 • 4 🎟 = 1 Video V3 generation 🎬✨
 • 1 🎟 = 1 Image 4K enhancement 🖼️4K
 • 1 🎟 = 1 Image-to-Image swap 🔄
 • 2 🎟 = 1 Video swap (template library) 🎬🔄
 • 2 🎟 = 1 Video swap (uploaded) 🎬📤


⚡️ Prioritize Coin deposits to receive more
Deposit methods are processed in order of priority:
Coin – Automatic, fast, many bonuses
PayPal – Automatic, flexible
Telegram – Slow, longer processing, less promotions

🔽 Please choose a payment method below:

🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us
👥 Group Onii AI: t.me/+YfJDrYjVxDg0ZGNl
👥 Group Onii Shop: t.me/+42AoYLMxXIBiNWNl
📡 Channel Onii AI: t.me/+hyrrhLAK02Y1NTdl
📡 Channel Onii Hub: t.me/+mRmEqqKZwwUyM2Q1
📡 Channel Onii XXX: t.me/+sCWoT_eYdVcyMGQ1"""

# Affiliate money text
AFFILIATE_TITLE = "🔗 Share & Earn"
AFFILIATE_TEXT = """Invite your friends and earn tickets!

- Share this link to get 1🎟:
{ref_link}

You have invited {count} friends so far."""

# Free credit text
FREE_CREDIT_TITLE = "🎁 How to Earn Free Credits"
FREE_CREDIT_TEXT = """Take advantage of these simple ways to get more tickets — no payment required
 • 1. Invite your friends – Earn tickets for every friend who joins through your link
 • 2. Check in daily – Receive 1 🎟 free ticket just for using the bot each day

Start earning and enjoy more creations, on us!"""

# Terms text
TERMS_TITLE = "📜 View Terms of Service"
TERMS_TEXT = """Terms of Service will be displayed here. Please contact admin for details."""
TERMS_ACCEPTED = "Thank you for accepting our Terms of Service. You can now use all features of the bot."

# Daily check-in messages
DAILY_CHECKIN_SUCCESS = "✅ Daily check-in successful! You received 1 🎟 ticket."
DAILY_CHECKIN_COOLDOWN = "You've already checked in today! Come back in {time}"

# Payment stubs for other methods
CRYPTO_MSG = "Crypto payment coming soon."
PAYPAL_MSG = "PayPal payment coming soon."

# Telegram Stars payment texts
STARS_PAYMENT_HEADER = """⭐ Telegram Stars Payment

Choose a package to purchase tickets:

💡 Benefits of Stars Payment:
• Fast & Secure
• Instant Processing
• Official Telegram Payment
• No Extra Fees

Select a package below:"""

PAYMENT_INSTRUCTIONS = """💎 {package}

💰 Price: {stars} ⭐ Stars (${usd})
🎟️ You'll receive: {tickets} tickets

📋 How to pay:
1️⃣ Click 'Pay with Stars' button
2️⃣ Complete payment in Telegram
3️⃣ Click 'I Paid - Verify' to check status

⚡️ Payment is processed instantly!"""

PAYMENT_PENDING = """⏳ Payment Not Detected Yet

Price: {stars} ⭐ Stars
Tickets: {tickets} 🎟️

Please complete the payment first, then click 'Check Again'.

Note: It may take a few seconds to process after payment."""

PAYMENT_CONFIRMED = """✅ Payment Confirmed!

Amount: {stars} ⭐ Stars
Tickets Credited: {tickets} 🎟️
Paid at: {paid_at}
Transaction ID: {transaction_id}

🎉 Your tickets have been added to your account!
Thank you for your purchase! 💝"""

PAYMENT_HISTORY_HEADER = "📊 Your Payment History:\n"
PAYMENT_HISTORY_EMPTY = "📊 Payment History\n\nYou haven't made any payments yet."

# Crypto payment texts
CRYPTO_PAYMENT_HEADER = """🪙 Crypto Payment

Choose a package to purchase tickets:

💡 Benefits of Crypto Payment:
• Fast & Secure
• Multiple Cryptocurrencies
• Low Fees
• Instant Processing

Supported currencies: USDT, TON, BTC, ETH, LTC, BNB, TRX, USDC

Select a package below:"""

CRYPTO_INVOICE_CREATED = """💵 Crypto Invoice Created!

💰 Amount: {amount} {currency}
🎟️ You'll receive: {tickets} tickets
🔖 Invoice ID: {invoice_id}

📋 How to pay:
1️⃣ Click 'Pay Invoice' button
2️⃣ Complete payment via @send
3️⃣ Click 'Check Status' to verify

⚡️ Payment is processed automatically!"""

CRYPTO_INVOICE_PENDING = """⏳ Payment Pending

Amount: {amount} {currency}
Tickets: {tickets} 🎟️
Status: {status}

Please complete the payment first, then click 'Check Again'.

Note: It may take a few minutes to process after payment."""

CRYPTO_INVOICE_CONFIRMED = """✅ Payment Confirmed!

Amount: {amount} {currency}
Tickets Credited: {tickets} 🎟️
Paid at: {paid_at}
Invoice ID: {invoice_id}

🎉 Your tickets have been added to your account!
Thank you for your payment! 💝"""

CRYPTO_INVOICE_EXPIRED = """⏰ Invoice Expired

This invoice has expired.
Please create a new invoice to continue."""

CRYPTO_CUSTOM_INVOICE = """💰 Custom Crypto Invoice

Send amount in format:
/invoice <amount> <currency>

Examples:
• /invoice 10 USDT
• /invoice 0.1 TON
• /invoice 0.0001 BTC

Supported: USDT, TON, BTC, ETH, LTC, BNB, TRX, USDC"""

CRYPTO_HISTORY_HEADER = "📊 Your Crypto Payment History:\n"
CRYPTO_HISTORY_EMPTY = "📊 Crypto Payment History\n\nYou haven't made any crypto payments yet."

# Unified payment history templates
UNIFIED_PAYMENT_HISTORY_HEADER = "📊 Payment History (Page {page} of {total})\n\n"
UNIFIED_PAYMENT_HISTORY_EMPTY = "📊 Payment History\n\nYou haven't made any payments yet."

# Welcome messages
WELCOME_NEW = "Welcome! You've been granted $0.10 balance and 1 ticket to get started."
WELCOME_BACK = "Welcome back! Here's your main menu:"

