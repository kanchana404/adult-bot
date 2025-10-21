"""Activity tracking middleware to update user's last_activity timestamp."""
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.db.repositories import UserRepository

logger = logging.getLogger(__name__)

class ActivityTrackerMiddleware(BaseMiddleware):
    """Middleware to track user activity and update last_activity timestamp."""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Update user's last_activity timestamp on every interaction."""
        try:
            # Get user ID from the event
            if isinstance(event, Message):
                user_id = event.from_user.id
                # Skip updating activity for /start commands - let the start handler manage this
                if event.text and event.text.startswith('/start'):
                    logger.debug(f"Skipping activity update for /start command from user {user_id}")
                    return await handler(event, data)
            elif isinstance(event, CallbackQuery):
                user_id = event.from_user.id
            else:
                # Skip if we can't get user ID
                return await handler(event, data)
            
            # Update last activity timestamp
            user_repo = UserRepository()
            await user_repo.update_last_activity(user_id)
            logger.debug(f"Updated last_activity for user {user_id}")
            
        except Exception as e:
            logger.warning(f"Failed to update last_activity: {e}")
        
        # Continue to the next handler
        return await handler(event, data)
