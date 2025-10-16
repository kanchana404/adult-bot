"""Formatting utilities for the bot."""
from decimal import Decimal
from typing import Union

def format_currency(amount: Union[str, float, Decimal]) -> str:
    """Format currency to 2 decimal places."""
    if isinstance(amount, str):
        amount = Decimal(amount)
    elif isinstance(amount, float):
        amount = Decimal(str(amount))
    
    return f"{amount:.2f}"

def format_decimal_string(amount: Union[str, float, Decimal]) -> str:
    """Format decimal to string with 2 decimal places."""
    if isinstance(amount, str):
        amount = Decimal(amount)
    elif isinstance(amount, float):
        amount = Decimal(str(amount))
    
    return f"{amount:.2f}"

def add_decimal_strings(a: str, b: str) -> str:
    """Add two decimal strings and return as decimal string."""
    return format_decimal_string(Decimal(a) + Decimal(b))

