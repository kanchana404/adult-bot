"""Database models for the Telegram bot."""
from typing import TypedDict, Optional, Literal
from datetime import datetime
from bson import ObjectId

class User(TypedDict):
    """User document model."""
    _id: int  # Telegram user ID
    created_at: datetime
    account_id: int  # Same as _id
    balance_usd: str  # Decimal string
    tickets: int
    vip_tickets: int
    lucky_spins: int
    referrer_id: Optional[int]
    referral_count: int
    referral_ticket_earned: str  # Decimal string
    accepted_terms: bool
    last_daily_checkin_at: Optional[datetime]
    language: str  # User's preferred language code
    last_activity: Optional[datetime]  # Last time user interacted with the bot

class Referral(TypedDict):
    """Referral document model."""
    _id: ObjectId
    referrer_id: int
    referred_user_id: int
    created_at: datetime

class Transaction(TypedDict):
    """Transaction document model."""
    _id: ObjectId
    user_id: int
    type: Literal["bonus", "credit", "debit", "payment"]
    amount_tickets: Optional[int]
    amount_usd: Optional[str]  # Decimal string
    meta: dict
    created_at: datetime

class Payment(TypedDict):
    """Payment document model for tracking Telegram Stars payments."""
    _id: ObjectId
    user_id: int
    username: Optional[str]
    payload: str  # Unique payload for this payment
    stars_amount: int  # Amount in Telegram Stars
    tickets_amount: int  # Tickets to be credited
    usd_amount: str  # USD equivalent (Decimal string)
    payment_url: str  # Invoice URL
    status: Literal["pending", "paid", "cancelled"]
    created_at: datetime
    paid_at: Optional[datetime]
    telegram_payment_id: Optional[str]  # Telegram's payment charge ID

class CryptoInvoice(TypedDict):
    """Crypto invoice document model for tracking crypto payments."""
    _id: ObjectId
    user_id: int
    username: Optional[str]
    invoice_id: str  # CryptoBot invoice ID
    amount: float  # Amount in crypto currency
    currency: str  # Currency code (USDT, TON, BTC, etc.)
    description: str  # Invoice description
    payment_url: str  # Payment URL
    status: Literal["active", "paid", "expired", "cancelled"]
    created_at: datetime
    paid_at: Optional[datetime]
    payload: str  # Unique payload for this invoice
    tickets_amount: int  # Tickets to be credited
    usd_amount: str  # USD equivalent (Decimal string)

class UnifiedPaymentHistory(TypedDict):
    """Unified payment history model combining stars and crypto payments."""
    _id: ObjectId
    user_id: int
    username: Optional[str]
    payment_type: Literal["stars", "crypto"]
    payment_id: str  # Either payload (stars) or invoice_id (crypto)
    amount: str  # Amount in original currency (stars count or crypto amount)
    currency: str  # Currency (stars, USDT, TON, BTC, etc.)
    tickets_amount: int  # Tickets credited
    usd_amount: str  # USD equivalent (Decimal string)
    status: Literal["pending", "paid", "cancelled", "active", "expired"]
    created_at: datetime
    paid_at: Optional[datetime]
    description: str  # Payment description

