"""Repository layer for database operations."""
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from bot.db.mongo import get_database
from bot.db.models import User, Referral, Transaction, Payment

class UserRepository:
    """Repository for user operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().users
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return await self.collection.find_one({"_id": user_id})
    
    async def create_user(self, user: User) -> None:
        """Create a new user."""
        await self.collection.insert_one(user)
    
    async def update_user(self, user_id: int, update_data: dict) -> None:
        """Update user data."""
        await self.collection.update_one({"_id": user_id}, {"$set": update_data})
    
    async def increment_referral_count(self, user_id: int) -> None:
        """Increment user's referral count."""
        await self.collection.update_one(
            {"_id": user_id}, 
            {"$inc": {"referral_count": 1}}
        )
    
    async def add_referral_tickets(self, user_id: int, tickets: str) -> None:
        """Add tickets to user's referral earnings."""
        await self.collection.update_one(
            {"_id": user_id}, 
            {"$inc": {"tickets": 1, "referral_ticket_earned": float(tickets)}}
        )
    
    async def increment_tickets(self, user_id: int, amount: int) -> None:
        """Increment user's tickets."""
        await self.collection.update_one(
            {"_id": user_id}, 
            {"$inc": {"tickets": amount}}
        )

class ReferralRepository:
    """Repository for referral operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().referrals
    
    async def create_referral(self, referrer_id: int, referred_user_id: int) -> None:
        """Create a referral record."""
        referral: Referral = {
            "_id": ObjectId(),
            "referrer_id": referrer_id,
            "referred_user_id": referred_user_id,
            "created_at": datetime.utcnow()
        }
        await self.collection.insert_one(referral)
    
    async def get_referral_count(self, user_id: int) -> int:
        """Get referral count for a user."""
        return await self.collection.count_documents({"referrer_id": user_id})
    
    async def check_referral_exists(self, referrer_id: int, referred_user_id: int) -> bool:
        """Check if referral already exists."""
        return await self.collection.find_one({
            "referrer_id": referrer_id,
            "referred_user_id": referred_user_id
        }) is not None

class TransactionRepository:
    """Repository for transaction operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().transactions
    
    async def create_transaction(self, transaction: Transaction) -> None:
        """Create a new transaction."""
        await self.collection.insert_one(transaction)
    
    async def get_user_transactions(self, user_id: int, limit: int = 100) -> List[Transaction]:
        """Get user's transactions."""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

class PaymentRepository:
    """Repository for payment operations."""
    
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_database().payments
    
    async def create_payment(self, payment: Payment) -> None:
        """Create a new payment record."""
        await self.collection.insert_one(payment)
    
    async def get_payment_by_payload(self, payload: str) -> Optional[Payment]:
        """Get payment by payload."""
        return await self.collection.find_one({"payload": payload})
    
    async def update_payment_status(self, payload: str, telegram_payment_id: str) -> None:
        """Mark payment as paid."""
        await self.collection.update_one(
            {"payload": payload},
            {
                "$set": {
                    "status": "paid",
                    "paid_at": datetime.utcnow(),
                    "telegram_payment_id": telegram_payment_id
                }
            }
        )
    
    async def get_user_payments(self, user_id: int, limit: int = 50) -> List[Payment]:
        """Get user's payment history."""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def cancel_payment(self, payload: str) -> None:
        """Cancel a payment."""
        await self.collection.update_one(
            {"payload": payload},
            {"$set": {"status": "cancelled"}}
        )

