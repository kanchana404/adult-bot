"""Economy service for handling balance and tickets."""
import logging
from typing import Optional
from bot.db.repositories import UserRepository, TransactionRepository
from bot.db.models import User, Transaction
from bot.utils.formatting import add_decimal_strings, format_currency
from bot.utils.time import utc_now
from bson import ObjectId

logger = logging.getLogger(__name__)

class EconomyService:
    """Service for handling economy operations."""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.transaction_repo = TransactionRepository()
    
    async def add_tickets(self, user_id: int, amount: int, transaction_type: str = "bonus", meta: dict = None) -> bool:
        """
        Add tickets to user's account.
        
        Args:
            user_id: User ID
            amount: Number of tickets to add
            transaction_type: Type of transaction
            meta: Additional metadata
            
        Returns:
            bool: True if successful
        """
        try:
            # Update user tickets using increment method
            await self.user_repo.increment_tickets(user_id, amount)
            
            # Create transaction record
            transaction: Transaction = {
                "_id": ObjectId(),
                "user_id": user_id,
                "type": transaction_type,
                "amount_tickets": amount,
                "amount_usd": None,
                "meta": meta or {},
                "created_at": utc_now()
            }
            await self.transaction_repo.create_transaction(transaction)
            
            logger.info(f"Added {amount} tickets to user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding tickets to user {user_id}: {e}")
            return False
    
    async def add_balance(self, user_id: int, amount: str, transaction_type: str = "credit", meta: dict = None) -> bool:
        """
        Add balance to user's account.
        
        Args:
            user_id: User ID
            amount: Amount to add (as decimal string)
            transaction_type: Type of transaction
            meta: Additional metadata
            
        Returns:
            bool: True if successful
        """
        try:
            # Get current user
            user = await self.user_repo.get_user(user_id)
            if not user:
                return False
            
            # Calculate new balance
            new_balance = add_decimal_strings(user["balance_usd"], amount)
            
            # Update user balance
            await self.user_repo.update_user(user_id, {"balance_usd": new_balance})
            
            # Create transaction record
            transaction: Transaction = {
                "_id": ObjectId(),
                "user_id": user_id,
                "type": transaction_type,
                "amount_tickets": None,
                "amount_usd": amount,
                "meta": meta or {},
                "created_at": utc_now()
            }
            await self.transaction_repo.create_transaction(transaction)
            
            logger.info(f"Added ${amount} to user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding balance to user {user_id}: {e}")
            return False
    
    async def get_user_economy(self, user_id: int) -> Optional[dict]:
        """Get user's economy data."""
        user = await self.user_repo.get_user(user_id)
        if not user:
            return None
        
        return {
            "balance_usd": user["balance_usd"],
            "tickets": user["tickets"],
            "vip_tickets": user["vip_tickets"],
            "lucky_spins": user["lucky_spins"],
            "referral_ticket_earned": user["referral_ticket_earned"]
        }


