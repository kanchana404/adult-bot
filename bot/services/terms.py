"""Terms of service management."""
import logging
from bot.db.repositories import UserRepository

logger = logging.getLogger(__name__)

class TermsService:
    """Service for handling terms of service."""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    async def has_accepted_terms(self, user_id: int) -> bool:
        """Check if user has accepted terms of service."""
        try:
            user = await self.user_repo.get_user(user_id)
            if not user:
                return False
            return user.get("accepted_terms", False)
        except Exception as e:
            logger.error(f"Error checking terms acceptance for user {user_id}: {e}")
            return False
    
    async def accept_terms(self, user_id: int) -> bool:
        """Mark user as having accepted terms of service."""
        try:
            await self.user_repo.update_user(user_id, {"$set": {"accepted_terms": True}})
            logger.info(f"User {user_id} accepted terms of service")
            return True
        except Exception as e:
            logger.error(f"Error accepting terms for user {user_id}: {e}")
            return False


