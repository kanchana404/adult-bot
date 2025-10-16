"""Configuration module for the Telegram bot."""
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# Required environment variables
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
MONGODB_URI: str = os.getenv("MONGODB_URI", "")
MONGODB_DB: str = os.getenv("MONGODB_DB", "")

# Optional environment variables
ADMIN_IDS: List[int] = []
if admin_ids_str := os.getenv("ADMIN_IDS"):
    ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",")]

BOT_PUBLIC_USERNAME: Optional[str] = os.getenv("BOT_PUBLIC_USERNAME")

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is required")
if not MONGODB_DB:
    raise ValueError("MONGODB_DB environment variable is required")

