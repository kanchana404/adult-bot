"""Language system for the Telegram bot."""
from typing import Dict, Any

# Supported languages with their codes and display names
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "flag": "🇬🇧"},
    "vi": {"name": "Việt Nam", "flag": "🇻🇳"},
    "es": {"name": "Spanish", "flag": "🇪🇸"},
    "fr": {"name": "French", "flag": "🇫🇷"},
    "de": {"name": "German", "flag": "🇩🇪"},
    "zh": {"name": "Chinese", "flag": "🇨🇳"},
    "ru": {"name": "Russian", "flag": "🇷🇺"},
    "ar": {"name": "Arabic", "flag": "🇸🇦"},
    "pt": {"name": "Portuguese", "flag": "🇵🇹"},
    "it": {"name": "Italian", "flag": "🇮🇹"},
    "ja": {"name": "Japanese", "flag": "🇯🇵"},
    "ko": {"name": "Korean", "flag": "🇰🇷"},
    "hi": {"name": "Hindi", "flag": "🇮🇳"},
    "tr": {"name": "Turkish", "flag": "🇹🇷"},
    "si": {"name": "Sinhala", "flag": "🇱🇰"},
    "nl": {"name": "Dutch", "flag": "🇳🇱"},
}

DEFAULT_LANGUAGE = "en"

# Translation texts for all languages
TRANSLATIONS = {
    "en": {
        "main_menu": {
            "profile": "Profile",
            "language": "Language",
            "topup": "🎟 Top up Credit",
            "affiliate": "🤑 Affiliate money",
            "free_credit": "🎟 Get Free Credit",
            "terms": "📄 Terms"
        },
        "language_selection": {
            "title": "Select your preferred language:",
            "back": "⬅️ Back to Main",
            "confirmation": "{flag} Language changed to {name}!\n\nAll text and buttons will now be in {name}.",
            "set_to": "Language set to {name}"
        },
        "profile": {
            "title": "💼 Account ID: {account_id}\n\n💵Balance: ${balance}\n💎You have {tickets} tickets, of which {vip}🏆 VIP spins are not\n🎰Lucky spins: {lucky}\n\nYou have earned {ref_tickets:.2f} tickets from referrals\n\nYou have invited {invited} people"
        },
        "welcome": {
            "new": "Welcome! You've been granted $0.10 balance and 1 ticket to get started.",
            "back": "Welcome back! Here's your main menu:"
        },
        "topup": {
            "title": "🎟 Top up Credit\nTOP UP CREDIT $ PAYMENT OPTION\n\n💼 Account ID: {account_id}\n💵 Balance: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Lucky spins: {lucky}\n\n⚙️ Usage Details:\n • 1 🎟 = 1 AI-generated image 🖼\n • 2 🎟 = 1 Video V1 generation 🎬\n • 4 🎟 = 1 Video V2 generation 🎬✨\n • 4 🎟 = 1 Video V3 generation 🎬✨\n • 1 🎟 = 1 Image 4K enhancement 🖼️4K\n • 1 🎟 = 1 Image-to-Image swap 🔄\n • 2 🎟 = 1 Video swap (template library) 🎬🔄\n • 2 🎟 = 1 Video swap (uploaded) 🎬📤\n\n\n⚡️ Prioritize Coin deposits to receive more\nDeposit methods are processed in order of priority:\nCoin – Automatic, fast, many bonuses\nPayPal – Automatic, flexible\nTelegram – Slow, longer processing, less promotions\n\n🔽 Please choose a payment method below:\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Group Onii AI: t.me/+YfJDrYjVxDg0ZGNl\n👥 Group Onii Shop: t.me/+42AoYLMxXIBiNWNl\n📡 Channel Onii AI: t.me/+hyrrhLAK02Y1NTdl\n📡 Channel Onii Hub: t.me/+mRmEqqKZwwUyM2Q1\n📡 Channel Onii XXX: t.me/+sCWoT_eYdVcyMGQ1"
        },
        "affiliate": {
            "title": "🔗 Share & Earn",
            "text": "Invite your friends and earn tickets!\n\n- Share this link to get 1🎟:\n{ref_link}\n\nYou have invited {count} friends so far."
        },
        "free_credit": {
            "title": "🎁 How to Earn Free Credits",
            "text": "Take advantage of these simple ways to get more tickets — no payment required\n • 1. Invite your friends – Earn tickets for every friend who joins through your link\n • 2. Check in daily – Receive 1 🎟 free ticket just for using the bot each day\n\nStart earning and enjoy more creations, on us!"
        },
        "terms": {
            "title": "📜 View Terms of Service",
            "text": "Terms of Service will be displayed here. Please contact admin for details.",
            "accepted": "Thank you for accepting our Terms of Service. You can now use all features of the bot."
        },
        "daily": {
            "success": "✅ Daily check-in successful! You received 1 🎟 ticket.",
            "cooldown": "You've already checked in today! Come back in {time}"
        },
        "payment": {
            "telegram_stars": "Telegram Stars payment coming soon.",
            "crypto": "Crypto payment coming soon.",
            "paypal": "PayPal payment coming soon."
        }
    },
    # Add other languages here - for now, all will use English as fallback
    "vi": {
        "main_menu": {
            "profile": "Hồ sơ",
            "language": "Ngôn ngữ",
            "topup": "🎟 Nạp tiền",
            "affiliate": "🤑 Tiền liên kết",
            "free_credit": "🎟 Nhận tín dụng miễn phí",
            "terms": "📄 Điều khoản"
        },
        "language_selection": {
            "title": "Chọn ngôn ngữ ưa thích của bạn:",
            "back": "⬅️ Quay lại Menu chính",
            "confirmation": "{flag} Ngôn ngữ đã thay đổi thành {name}!\n\nTất cả văn bản và nút bấm giờ sẽ hiển thị bằng {name}.",
            "set_to": "Ngôn ngữ đã đặt thành {name}"
        },
        "welcome": {
            "new": "Chào mừng! Bạn đã được cấp số dư $0.10 và 1 vé để bắt đầu.",
            "back": "Chào mừng trở lại! Đây là menu chính của bạn:"
        }
    },
    "es": {
        "main_menu": {
            "profile": "Perfil",
            "language": "Idioma",
            "topup": "🎟 Recargar Crédito",
            "affiliate": "🤑 Dinero Afiliado",
            "free_credit": "🎟 Obtener Crédito Gratis",
            "terms": "📄 Términos"
        },
        "language_selection": {
            "title": "Selecciona tu idioma preferido:",
            "back": "⬅️ Volver al Menú Principal",
            "confirmation": "{flag} ¡Idioma cambiado a {name}!\n\nTodo el texto y botones ahora estarán en {name}.",
            "set_to": "Idioma establecido a {name}"
        },
        "welcome": {
            "new": "¡Bienvenido! Se te ha otorgado un saldo de $0.10 y 1 ticket para comenzar.",
            "back": "¡Bienvenido de nuevo! Aquí está tu menú principal:"
        }
    },
    "fr": {
        "main_menu": {
            "profile": "Profil",
            "language": "Langue",
            "topup": "🎟 Recharger Crédit",
            "affiliate": "🤑 Argent Partenaire",
            "free_credit": "🎟 Obtenir Crédit Gratuit",
            "terms": "📄 Conditions"
        },
        "language_selection": {
            "title": "Sélectionnez votre langue préférée:",
            "back": "⬅️ Retour au Menu Principal",
            "confirmation": "{flag} Langue changée en {name}!\n\nTout le texte et les boutons seront maintenant en {name}.",
            "set_to": "Langue définie sur {name}"
        },
        "welcome": {
            "new": "Bienvenue ! Vous avez reçu un solde de 0,10 $ et 1 ticket pour commencer.",
            "back": "Bon retour ! Voici votre menu principal :"
        }
    }
}

def get_text(language: str, key: str, **kwargs) -> str:
    """Get translated text for a given language and key."""
    if language not in TRANSLATIONS:
        language = DEFAULT_LANGUAGE
    
    # Navigate through nested keys (e.g., "main_menu.profile")
    keys = key.split('.')
    text = TRANSLATIONS.get(language, TRANSLATIONS[DEFAULT_LANGUAGE])
    
    for k in keys:
        if isinstance(text, dict) and k in text:
            text = text[k]
        else:
            # Fallback to English
            text = TRANSLATIONS[DEFAULT_LANGUAGE]
            for k in keys:
                if isinstance(text, dict) and k in text:
                    text = text[k]
                else:
                    return f"[Missing translation: {key}]"
            break
    
    if isinstance(text, str):
        return text.format(**kwargs) if kwargs else text
    else:
        return f"[Invalid translation: {key}]"

def get_language_name(language_code: str) -> str:
    """Get display name for a language code."""
    return SUPPORTED_LANGUAGES.get(language_code, {}).get("name", "English")

def get_language_flag(language_code: str) -> str:
    """Get flag emoji for a language code."""
    return SUPPORTED_LANGUAGES.get(language_code, {}).get("flag", "🇬🇧")
