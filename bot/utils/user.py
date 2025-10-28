"""User utility functions."""
from typing import Optional
from bot.db.models import User
from bot.config import ADMIN_IDS

def is_vip_user(user: Optional[User]) -> bool:
    """Check if user is VIP based on vip_tickets."""
    if not user:
        return False
    return user.get("vip_tickets", 0) > 0

def is_admin_user(user_id: int) -> bool:
    """Check if user is an admin."""
    return user_id in ADMIN_IDS


