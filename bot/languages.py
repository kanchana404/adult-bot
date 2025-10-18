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
    },
    "hi": {
        "main_menu": {
            "profile": "प्रोफ़ाइल",
            "language": "भाषा",
            "topup": "🎟 क्रेडिट टॉप अप",
            "affiliate": "🤑 सहयोगी पैसा",
            "free_credit": "🎟 मुफ्त क्रेडिट प्राप्त करें",
            "terms": "📄 नियम और शर्तें"
        },
        "language_selection": {
            "title": "अपनी पसंदीदा भाषा चुनें:",
            "back": "⬅️ मुख्य मेनू पर वापस जाएं",
            "confirmation": "{flag} भाषा {name} में बदल दी गई!\n\nसभी टेक्स्ट और बटन अब {name} में होंगे।",
            "set_to": "भाषा {name} पर सेट की गई"
        },
        "welcome": {
            "new": "स्वागत है! आपको शुरुआत के लिए $0.10 बैलेंस और 1 टिकट दिया गया है।",
            "back": "वापस स्वागत है! यहां आपका मुख्य मेनू है:"
        }
    },
    "si": {
        "main_menu": {
            "profile": "පැතිකඩ",
            "language": "භාෂාව",
            "topup": "🎟 ක්‍රෙඩිට් ටොප් අප්",
            "affiliate": "🤑 සහකරු මුදල්",
            "free_credit": "🎟 නොමිලේ ක්‍රෙඩිට් ලබා ගන්න",
            "terms": "📄 නියමයන්"
        },
        "language_selection": {
            "title": "ඔබේ ප්‍රියතම භාෂාව තෝරන්න:",
            "back": "⬅️ ප්‍රධාන මෙනුවට ආපසු",
            "confirmation": "{flag} භාෂාව {name} වෙත වෙනස් කරන ලදී!\n\nසියලුම පෙළ සහ බොත්තම් දැන් {name} හි වනු ඇත।",
            "set_to": "භාෂාව {name} වෙත සැකසීය"
        },
        "welcome": {
            "new": "සාදරයෙන් පිළිගනිමු! ආරම්භ කිරීම සඳහා ඔබට $0.10 ශේෂය සහ 1 ටිකට් ලබා දී ඇත।",
            "back": "නැවත සාදරයෙන් පිළිගනිමු! මෙන්න ඔබේ ප්‍රධාන මෙනුව:"
        }
    },
    "de": {
        "main_menu": {
            "profile": "Profil",
            "language": "Sprache",
            "topup": "🎟 Guthaben aufladen",
            "affiliate": "🤑 Partner-Geld",
            "free_credit": "🎟 Kostenloses Guthaben erhalten",
            "terms": "📄 Bedingungen"
        },
        "language_selection": {
            "title": "Wählen Sie Ihre bevorzugte Sprache:",
            "back": "⬅️ Zurück zum Hauptmenü",
            "confirmation": "{flag} Sprache zu {name} geändert!\n\nAlle Texte und Buttons werden jetzt in {name} angezeigt.",
            "set_to": "Sprache auf {name} gesetzt"
        },
        "welcome": {
            "new": "Willkommen! Sie haben ein Guthaben von 0,10 $ und 1 Ticket zum Starten erhalten.",
            "back": "Willkommen zurück! Hier ist Ihr Hauptmenü:"
        }
    },
    "zh": {
        "main_menu": {
            "profile": "个人资料",
            "language": "语言",
            "topup": "🎟 充值积分",
            "affiliate": "🤑 联盟收入",
            "free_credit": "🎟 获取免费积分",
            "terms": "📄 条款"
        },
        "language_selection": {
            "title": "选择您的首选语言:",
            "back": "⬅️ 返回主菜单",
            "confirmation": "{flag} 语言已更改为 {name}!\n\n所有文本和按钮现在将显示为 {name}。",
            "set_to": "语言设置为 {name}"
        },
        "welcome": {
            "new": "欢迎！您已获得 $0.10 余额和 1 张票券开始使用。",
            "back": "欢迎回来！这是您的主菜单:"
        }
    },
    "ru": {
        "main_menu": {
            "profile": "Профиль",
            "language": "Язык",
            "topup": "🎟 Пополнить кредит",
            "affiliate": "🤑 Партнерские деньги",
            "free_credit": "🎟 Получить бесплатный кредит",
            "terms": "📄 Условия"
        },
        "language_selection": {
            "title": "Выберите предпочитаемый язык:",
            "back": "⬅️ Назад в главное меню",
            "confirmation": "{flag} Язык изменен на {name}!\n\nВесь текст и кнопки теперь будут на {name}.",
            "set_to": "Язык установлен на {name}"
        },
        "welcome": {
            "new": "Добро пожаловать! Вам предоставлен баланс $0.10 и 1 билет для начала.",
            "back": "Добро пожаловать обратно! Вот ваше главное меню:"
        }
    },
    "ar": {
        "main_menu": {
            "profile": "الملف الشخصي",
            "language": "اللغة",
            "topup": "🎟 شحن الرصيد",
            "affiliate": "🤑 أموال الشراكة",
            "free_credit": "🎟 الحصول على رصيد مجاني",
            "terms": "📄 الشروط"
        },
        "language_selection": {
            "title": "اختر لغتك المفضلة:",
            "back": "⬅️ العودة إلى القائمة الرئيسية",
            "confirmation": "{flag} تم تغيير اللغة إلى {name}!\n\nجميع النصوص والأزرار ستظهر الآن بـ {name}.",
            "set_to": "تم تعيين اللغة إلى {name}"
        },
        "welcome": {
            "new": "مرحباً! تم منحك رصيد $0.10 وتذكرة واحدة للبدء.",
            "back": "مرحباً بعودتك! إليك قائمتك الرئيسية:"
        }
    },
    "pt": {
        "main_menu": {
            "profile": "Perfil",
            "language": "Idioma",
            "topup": "🎟 Recarregar Crédito",
            "affiliate": "🤑 Dinheiro de Afiliado",
            "free_credit": "🎟 Obter Crédito Grátis",
            "terms": "📄 Termos"
        },
        "language_selection": {
            "title": "Selecione seu idioma preferido:",
            "back": "⬅️ Voltar ao Menu Principal",
            "confirmation": "{flag} Idioma alterado para {name}!\n\nTodo o texto e botões agora estarão em {name}.",
            "set_to": "Idioma definido para {name}"
        },
        "welcome": {
            "new": "Bem-vindo! Você recebeu um saldo de $0.10 e 1 ticket para começar.",
            "back": "Bem-vindo de volta! Aqui está seu menu principal:"
        }
    },
    "it": {
        "main_menu": {
            "profile": "Profilo",
            "language": "Lingua",
            "topup": "🎟 Ricarica Credito",
            "affiliate": "🤑 Denaro Partner",
            "free_credit": "🎟 Ottieni Credito Gratuito",
            "terms": "📄 Termini"
        },
        "language_selection": {
            "title": "Seleziona la tua lingua preferita:",
            "back": "⬅️ Torna al Menu Principale",
            "confirmation": "{flag} Lingua cambiata in {name}!\n\nTutti i testi e i pulsanti saranno ora in {name}.",
            "set_to": "Lingua impostata su {name}"
        },
        "welcome": {
            "new": "Benvenuto! Ti è stato concesso un saldo di $0.10 e 1 biglietto per iniziare.",
            "back": "Bentornato! Ecco il tuo menu principale:"
        }
    },
    "ja": {
        "main_menu": {
            "profile": "プロフィール",
            "language": "言語",
            "topup": "🎟 クレジットチャージ",
            "affiliate": "🤑 アフィリエイト収入",
            "free_credit": "🎟 無料クレジット取得",
            "terms": "📄 利用規約"
        },
        "language_selection": {
            "title": "お好みの言語を選択してください:",
            "back": "⬅️ メインメニューに戻る",
            "confirmation": "{flag} 言語が {name} に変更されました!\n\nすべてのテキストとボタンが {name} で表示されます。",
            "set_to": "言語が {name} に設定されました"
        },
        "welcome": {
            "new": "ようこそ！開始するために $0.10 の残高と 1 枚のチケットが付与されました。",
            "back": "おかえりなさい！こちらがメインメニューです:"
        }
    },
    "ko": {
        "main_menu": {
            "profile": "프로필",
            "language": "언어",
            "topup": "🎟 크레딧 충전",
            "affiliate": "🤑 제휴 수익",
            "free_credit": "🎟 무료 크레딧 받기",
            "terms": "📄 약관"
        },
        "language_selection": {
            "title": "선호하는 언어를 선택하세요:",
            "back": "⬅️ 메인 메뉴로 돌아가기",
            "confirmation": "{flag} 언어가 {name}로 변경되었습니다!\n\n모든 텍스트와 버튼이 이제 {name}로 표시됩니다.",
            "set_to": "언어가 {name}로 설정되었습니다"
        },
        "welcome": {
            "new": "환영합니다! 시작하기 위해 $0.10 잔액과 1장의 티켓이 부여되었습니다.",
            "back": "다시 오신 것을 환영합니다! 여기 메인 메뉴입니다:"
        }
    },
    "tr": {
        "main_menu": {
            "profile": "Profil",
            "language": "Dil",
            "topup": "🎟 Kredi Yükle",
            "affiliate": "🤑 Ortaklık Parası",
            "free_credit": "🎟 Ücretsiz Kredi Al",
            "terms": "📄 Şartlar"
        },
        "language_selection": {
            "title": "Tercih ettiğiniz dili seçin:",
            "back": "⬅️ Ana Menüye Dön",
            "confirmation": "{flag} Dil {name} olarak değiştirildi!\n\nTüm metinler ve butonlar artık {name} olarak görünecek.",
            "set_to": "Dil {name} olarak ayarlandı"
        },
        "welcome": {
            "new": "Hoş geldiniz! Başlamak için $0.10 bakiye ve 1 bilet verildi.",
            "back": "Tekrar hoş geldiniz! İşte ana menünüz:"
        }
    },
    "nl": {
        "main_menu": {
            "profile": "Profiel",
            "language": "Taal",
            "topup": "🎟 Krediet Opladen",
            "affiliate": "🤑 Partner Geld",
            "free_credit": "🎟 Gratis Krediet Krijgen",
            "terms": "📄 Voorwaarden"
        },
        "language_selection": {
            "title": "Selecteer uw voorkeurstaal:",
            "back": "⬅️ Terug naar Hoofdmenu",
            "confirmation": "{flag} Taal gewijzigd naar {name}!\n\nAlle tekst en knoppen zullen nu in {name} zijn.",
            "set_to": "Taal ingesteld op {name}"
        },
        "welcome": {
            "new": "Welkom! U heeft een saldo van $0.10 en 1 ticket gekregen om te beginnen.",
            "back": "Welkom terug! Hier is uw hoofdmenu:"
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
