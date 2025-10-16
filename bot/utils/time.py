"""Time utilities for the bot."""
from datetime import datetime, timezone
from typing import Tuple

def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)

def seconds_to_hms(seconds: int) -> str:
    """Convert seconds to HH:MM:SS format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def get_remaining_cooldown(last_checkin: datetime, cooldown_hours: int = 8) -> Tuple[bool, str]:
    """
    Check if user can check in and return remaining time.
    
    Returns:
        Tuple[bool, str]: (can_checkin, remaining_time)
    """
    now = utc_now()
    time_diff = now - last_checkin
    cooldown_seconds = cooldown_hours * 3600
    
    if time_diff.total_seconds() >= cooldown_seconds:
        return True, ""
    else:
        remaining_seconds = int(cooldown_seconds - time_diff.total_seconds())
        return False, seconds_to_hms(remaining_seconds)


