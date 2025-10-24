"""User utility functions."""
from bot.db.models import User

def is_vip_user(user: User) -> bool:
    """Check if user is VIP based on vip_tickets."""
    return user.get("vip_tickets", 0) > 0


