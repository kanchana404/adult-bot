"""Referral service for handling user referrals."""
import logging
from typing import Optional
from aiogram import Bot
from bot.config import BOT_TOKEN
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
            
            # Send notification to referrer
            await self.send_referral_notification(referrer_id, referred_user_id)
            
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
    
    async def send_referral_notification(self, referrer_id: int, referred_user_id: int) -> None:
        """Send notification to referrer about new referral."""
        try:
            # Get referred user info
            referred_user = await self.user_repo.get_user(referred_user_id)
            if not referred_user:
                logger.warning(f"Referred user {referred_user_id} not found for notification")
                return
            
            # Get referrer info
            referrer = await self.user_repo.get_user(referrer_id)
            if not referrer:
                logger.warning(f"Referrer {referrer_id} not found for notification")
                return
            
            # Create bot instance
            bot = Bot(token=BOT_TOKEN)
            
            # Format referred user name
            referred_name = referred_user.get("username", "Unknown")
            if referred_name == "Unknown":
                referred_name = f"User {referred_user_id}"
            else:
                referred_name = f"@{referred_name}"
            
            # Create notification message
            notification_text = (
                f"🎉 **New Referral!**\n\n"
                f"Congratulations! You got a new referral from {referred_name}!\n\n"
                f"✅ **Reward:** 1 ticket added to your account\n"
                f"📊 **Total Referrals:** {referrer['referral_count'] + 1}\n"
                f"🎟 **Referral Tickets Earned:** {float(referrer['referral_ticket_earned']) + 1.0:.2f}\n\n"
                f"Keep sharing your referral link to earn more tickets! 🚀"
            )
            
            # Send notification
            await bot.send_message(
                chat_id=referrer_id,
                text=notification_text,
                parse_mode="Markdown"
            )
            
            await bot.session.close()
            logger.info(f"Referral notification sent to {referrer_id}")
            
        except Exception as e:
            logger.error(f"Error sending referral notification to {referrer_id}: {e}")
            # Don't raise the exception to avoid breaking the referral process


