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

