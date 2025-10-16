"""Daily check-in service."""
import logging
from typing import Tuple
from bot.db.repositories import UserRepository
from bot.utils.time import utc_now, get_remaining_cooldown

logger = logging.getLogger(__name__)

class DailyService:
    """Service for handling daily check-ins."""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    async def can_checkin(self, user_id: int) -> Tuple[bool, str]:
        """
        Check if user can perform daily check-in.
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple[bool, str]: (can_checkin, remaining_time_or_message)
        """
        try:
            user = await self.user_repo.get_user(user_id)
            if not user:
                return False, "User not found"
            
            last_checkin = user.get("last_daily_checkin_at")
            if not last_checkin:
                return True, ""
            
            can_checkin, remaining_time = get_remaining_cooldown(last_checkin, cooldown_hours=8)
            return can_checkin, remaining_time
            
        except Exception as e:
            logger.error(f"Error checking daily eligibility for user {user_id}: {e}")
            return False, "Error checking eligibility"
    
    async def perform_checkin(self, user_id: int) -> bool:
        """
        Perform daily check-in for user.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if successful
        """
        try:
            # Check eligibility first
            can_checkin, _ = await self.can_checkin(user_id)
            if not can_checkin:
                return False
            
            # Update last check-in time
            await self.user_repo.update_user(user_id, {
                "last_daily_checkin_at": utc_now()
            })
            
            # Add 1 ticket
            from bot.services.economy import EconomyService
            economy_service = EconomyService()
            await economy_service.add_tickets(user_id, 1, "bonus", {"daily_checkin": True})
            
            logger.info(f"Daily check-in completed for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error performing daily check-in for user {user_id}: {e}")
            return False


