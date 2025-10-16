"""Admin handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.config import ADMIN_IDS
from bot.db.repositories import UserRepository, ReferralRepository

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("stats"))
async def admin_stats(message: Message) -> None:
    """Handle /stats command for admins."""
    user_id = message.from_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_IDS:
        await message.answer("You don't have permission to use this command.")
        return
    
    user_repo = UserRepository()
    referral_repo = ReferralRepository()
    
    try:
        # Get total user count
        total_users = await user_repo.collection.count_documents({})
        
        # Get total referrals
        total_referrals = await referral_repo.collection.count_documents({})
        
        # Get users with referrals
        users_with_referrals = await user_repo.collection.count_documents({"referral_count": {"$gt": 0}})
        
        stats_text = f"""📊 Bot Statistics

👥 Total Users: {total_users}
🔗 Total Referrals: {total_referrals}
👤 Users with Referrals: {users_with_referrals}"""
        
        await message.answer(stats_text)
        
    except Exception as e:
        logger.error(f"Error getting admin stats: {e}")
        await message.answer("Error retrieving statistics.")


