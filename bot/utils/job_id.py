"""Utility functions for generating job IDs."""
import random
import string

def generate_job_id(length: int = 12) -> str:
    """Generate random alphanumeric job ID."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


