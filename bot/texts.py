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

# Payment stubs
TELEGRAM_STARS_MSG = "Telegram Stars payment coming soon."
CRYPTO_MSG = "Crypto payment coming soon."
PAYPAL_MSG = "PayPal payment coming soon."

# Welcome messages
WELCOME_NEW = "Welcome! You've been granted $0.10 balance and 1 ticket to get started."
WELCOME_BACK = "Welcome back! Here's your main menu:"

