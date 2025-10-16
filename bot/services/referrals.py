"""Referral service for handling user referrals."""
import logging
from typing import Optional
from bot.db.repositories import UserRepository, ReferralRepository, TransactionRepository
from bot.db.models import User, Transaction
from bot.utils.formatting import add_decimal_strings
from bot.utils.time import utc_now
from bson import ObjectId

logger = logging.getLogger(__name__)

class ReferralService:
    """Service for handling referral logic."""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.referral_repo = ReferralRepository()
        self.transaction_repo = TransactionRepository()
    
    async def process_referral(self, referrer_id: int, referred_user_id: int) -> bool:
        """
        Process a referral between two users.
        
        Args:
            referrer_id: ID of the user who made the referral
            referred_user_id: ID of the user who was referred
            
        Returns:
            bool: True if referral was processed successfully, False otherwise
        """
        try:
            # Check if referrer exists
            referrer = await self.user_repo.get_user(referrer_id)
            if not referrer:
                logger.warning(f"Referrer {referrer_id} not found")
                return False
            
            # Check if referral already exists
            if await self.referral_repo.check_referral_exists(referrer_id, referred_user_id):
                logger.info(f"Referral already exists: {referrer_id} -> {referred_user_id}")
                return False
            
            # Create referral record
            await self.referral_repo.create_referral(referrer_id, referred_user_id)
            
            # Update referrer stats
            await self.user_repo.increment_referral_count(referrer_id)
            await self.user_repo.add_referral_tickets(referrer_id, "1.00")
            
            # Create transaction record
            transaction: Transaction = {
                "_id": ObjectId(),
                "user_id": referrer_id,
                "type": "bonus",
                "amount_tickets": 1,
                "amount_usd": None,
                "meta": {"referral": referred_user_id},
                "created_at": utc_now()
            }
            await self.transaction_repo.create_transaction(transaction)
            
            logger.info(f"Referral processed successfully: {referrer_id} -> {referred_user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing referral {referrer_id} -> {referred_user_id}: {e}")
            return False
    
    async def get_referral_count(self, user_id: int) -> int:
        """Get referral count for a user."""
        return await self.referral_repo.get_referral_count(user_id)
    
    async def get_referral_link(self, user_id: int, bot_username: str) -> str:
        """Generate referral link for a user."""
        return f"https://t.me/{bot_username}?start={user_id}"


