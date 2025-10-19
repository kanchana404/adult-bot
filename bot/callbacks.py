"""Callback data constants for inline keyboards."""

# Main menu callbacks
PROFILE = "profile"
TOPUP = "topup"
AFFILIATE = "affiliate"
FREE_CREDIT = "free_credit"
TERMS = "terms"

# Navigation callbacks
BACK_MAIN = "back_main"
BACK_PROFILE = "back_profile"

# Payment method callbacks
TELEGRAM_STARS = "telegram_stars"
CRYPTO = "crypto"
PAYPAL = "paypal"

# Affiliate callbacks
SHARE_LINK = "share_link"

# Free credit callbacks
INVITE_FRIENDS = "invite_friends"
DAILY_CHECKIN = "daily_checkin"

# Terms callbacks
VIEW_TERMS = "view_terms"
AGREE_TERMS = "agree_terms"

# Stars payment callbacks
STAR_PACKAGE_PREFIX = "star_pkg_"  # Format: star_pkg_{index}
VERIFY_PAYMENT_PREFIX = "verify_pay_"  # Format: verify_pay_{payload}
CHECK_PAYMENT_HISTORY = "check_payment_history"

# Crypto payment callbacks
CRYPTO_PACKAGE_PREFIX = "crypto_pkg_"  # Format: crypto_pkg_{index}
CHECK_CRYPTO_INVOICE_PREFIX = "check_crypto_"  # Format: check_crypto_{invoice_id}
CHECK_CRYPTO_HISTORY = "check_crypto_history"
CREATE_CUSTOM_CRYPTO = "create_custom_crypto"

# Unified payment history callbacks
UNIFIED_PAYMENT_HISTORY = "unified_payment_history"
UNIFIED_PAYMENT_PAGE_PREFIX = "unified_page_"  # Format: unified_page_{page_number}

