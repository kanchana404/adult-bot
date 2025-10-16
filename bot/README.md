# Telegram Bot - Onii AI

A production-ready Telegram bot built with aiogram v3 and MongoDB, featuring user state persistence, referral system, daily check-ins, and payment integration stubs.

## Features

- **User Management**: Balance, tickets, VIP spins, lucky spins tracking
- **Referral System**: Deep linking with automatic referral attribution
- **Daily Check-ins**: 8-hour cooldown system with ticket rewards
- **Payment Integration**: Stubs for Telegram Stars, Crypto, and PayPal
- **Terms of Service**: User agreement tracking
- **Admin Panel**: Statistics and user management

## Tech Stack

- **Python**: 3.11+
- **Framework**: aiogram v3
- **Database**: MongoDB with Motor (async driver)
- **Environment**: python-dotenv
- **Logging**: Built-in logging module

## Project Structure

```
bot/
├── __init__.py
├── config.py              # Environment configuration
├── main.py                # Bot entry point
├── keyboards.py           # Inline keyboard builders
├── texts.py               # Message templates
├── callbacks.py           # Callback data constants
├── db/
│   ├── __init__.py
│   ├── mongo.py           # MongoDB connection & indexes
│   ├── repositories.py    # CRUD operations
│   └── models.py          # Document schemas
├── handlers/
│   ├── __init__.py
│   ├── start.py           # /start command & deep linking
│   ├── profile.py         # User profile display
│   ├── topup.py           # Payment methods
│   ├── affiliate.py       # Referral system
│   ├── free_credit.py     # Daily check-ins
│   ├── terms.py           # Terms of service
│   └── admin.py           # Admin commands
├── services/
│   ├── __init__.py
│   ├── referrals.py       # Referral logic
│   ├── economy.py         # Balance & ticket management
│   ├── daily.py           # Daily check-in logic
│   ├── payments.py        # Payment stubs
│   └── terms.py           # Terms management
└── utils/
    ├── __init__.py
    ├── formatting.py      # Currency formatting
    └── time.py            # Time utilities
```

## Setup Instructions

### 1. MongoDB Setup

1. Create a MongoDB Atlas account or set up a local MongoDB instance
2. Create a database (e.g., `onii_bot`)
3. Get your connection string

### 2. Environment Configuration

1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your values:
   ```env
   BOT_TOKEN=your_bot_token_here
   MONGODB_URI=mongodb+srv://user:pass@cluster/db?retryWrites=true&w=majority
   MONGODB_DB=onii_bot
   ADMIN_IDS=123456789,987654321
   BOT_PUBLIC_USERNAME=YourBotUsername
   ```

### 3. Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the bot:
   ```bash
   python -m bot.main
   ```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Telegram bot token from @BotFather |
| `MONGODB_URI` | Yes | MongoDB connection string |
| `MONGODB_DB` | Yes | Database name |
| `ADMIN_IDS` | No | Comma-separated admin user IDs |
| `BOT_PUBLIC_USERNAME` | No | Bot username fallback |

## Database Schema

### Users Collection
```json
{
  "_id": 1069535676,
  "created_at": "2024-01-01T00:00:00Z",
  "account_id": 1069535676,
  "balance_usd": "0.10",
  "tickets": 1,
  "vip_tickets": 0,
  "lucky_spins": 0,
  "referrer_id": 123456789,
  "referral_count": 0,
  "referral_ticket_earned": "0.00",
  "accepted_terms": false,
  "last_daily_checkin_at": null
}
```

### Referrals Collection
```json
{
  "_id": ObjectId("..."),
  "referrer_id": 123,
  "referred_user_id": 456,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Transactions Collection
```json
{
  "_id": ObjectId("..."),
  "user_id": 1069535676,
  "type": "bonus",
  "amount_tickets": 1,
  "amount_usd": null,
  "meta": {},
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Bot Commands

- `/start [referrer_id]` - Start the bot with optional referral
- `/profile` - View user profile
- `/stats` - Admin statistics (admin only)

## Key Features

### Referral System
- Deep linking: `https://t.me/botname?start=user_id`
- One-time referral attribution
- Automatic ticket rewards for referrers

### Daily Check-ins
- 8-hour cooldown between check-ins
- 1 ticket reward per check-in
- Cooldown display in HH:MM:SS format

### Payment Integration
- Telegram Stars (stub)
- Crypto payments (stub)
- PayPal integration (stub)

## Development

### Adding New Handlers
1. Create handler file in `bot/handlers/`
2. Register router in `bot/main.py`
3. Add callback constants in `bot/callbacks.py`

### Adding New Services
1. Create service file in `bot/services/`
2. Implement business logic
3. Add to repository layer if needed

### Database Operations
- Use repository pattern for all DB operations
- All operations are async
- Proper error handling and logging

## Production Deployment

1. Set up MongoDB with proper indexes
2. Configure environment variables
3. Set up logging and monitoring
4. Deploy with process manager (PM2, systemd, etc.)

## License

This project is for educational and development purposes.

