"""Configuration module for the Telegram bot."""
import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from bot/.env file
load_dotenv("bot/.env")

# Required environment variables
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
MONGODB_URI: str = os.getenv("MONGODB_URI", "")
MONGODB_DB: str = os.getenv("MONGODB_DB", "")

# Optional environment variables
ADMIN_IDS: List[int] = []
if admin_ids_str := os.getenv("ADMIN_IDS"):
    ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",")]

# Support for ADMIN_USERIDS as well (for backward compatibility)
if admin_userids_str := os.getenv("ADMIN_USERIDS"):
    admin_userids = [int(x.strip()) for x in admin_userids_str.split(",")]
    ADMIN_IDS.extend(admin_userids)

BOT_PUBLIC_USERNAME: Optional[str] = os.getenv("BOT_PUBLIC_USERNAME")

# Crypto payment configuration
CRYPTO_BOT_API_TOKEN: str = os.getenv("CRYPTO_BOT_API_TOKEN", "")
CRYPTO_BOT_API_URL: str = os.getenv("CRYPTO_BOT_API_URL", "https://testnet-pay.crypt.bot/api")
SEND_BOT_USERNAME: str = os.getenv("SEND_BOT_USERNAME", "send")

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is required")
if not MONGODB_DB:
    raise ValueError("MONGODB_DB environment variable is required")

