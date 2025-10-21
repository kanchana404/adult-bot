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
            "new": "🙌 Welcome to Onii AI Bot!\nDiscover a world of unlimited creativity with our smart AI-powered photo & video editing tools.\nCustomize your style your way – fast, private, and powerful.\n\n💼 Account ID: {account_id}\n💵 Balance: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Lucky spins: {lucky}\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Group Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Group Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Channel Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Channel Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Channel Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Welcome to Onii AI Bot!\nDiscover a world of unlimited creativity with our smart AI-powered photo & video editing tools.\nCustomize your style your way – fast, private, and powerful.\n\n💼 Account ID: {account_id}\n💵 Balance: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Lucky spins: {lucky}\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Group Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Group Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Channel Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Channel Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Channel Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Important Notice: If the bot you are using is currently showing as deleted or disabled,\nplease click the button below to get detailed instructions.\n🤖 View the list of backup bots: @Onii1BackupBot\n🙌 The world's fastest video exchange bot – Share to earn 1.5 🎟 or share without limits 🎁 to receive cash rewards!\n\n🔞 Onii AI – Experimental Channel for AI Photo & Video Editing Tools Create adult content that matches your taste: sexy images, deepfake videos, 4K quality, 100% private. ⚡️ Exclusive tech not yet released – only for\n\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Group Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Group Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Channel Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Channel Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Channel Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "topup": {
            "title": "🎟 Top up Credit\nTOP UP CREDIT $ PAYMENT OPTION\n\n💼 Account ID: {account_id}\n💵 Balance: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Lucky spins: {lucky}\n\n⚙️ Usage Details:\n • 1 🎟 = 1 AI-generated image 🖼\n • 2 🎟 = 1 Video V1 generation 🎬\n • 4 🎟 = 1 Video V2 generation 🎬✨\n • 4 🎟 = 1 Video V3 generation 🎬✨\n • 1 🎟 = 1 Image 4K enhancement 🖼️4K\n • 1 🎟 = 1 Image-to-Image swap 🔄\n • 2 🎟 = 1 Video swap (template library) 🎬🔄\n • 2 🎟 = 1 Video swap (uploaded) 🎬📤\n\n\n⚡️ Prioritize Coin deposits to receive more\nDeposit methods are processed in order of priority:\nCoin – Automatic, fast, many bonuses\nPayPal – Automatic, flexible\nTelegram – Slow, longer processing, less promotions\n\n🔽 Please choose a payment method below:\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Group Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Group Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Channel Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Channel Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Channel Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Chào mừng đến với Onii AI Bot!\nKhám phá thế giới sáng tạo không giới hạn với các công cụ chỉnh sửa ảnh và video thông minh được hỗ trợ bởi AI.\nTùy chỉnh phong cách của bạn theo cách riêng – nhanh chóng, riêng tư và mạnh mẽ.\n\n💼 ID Tài khoản: {account_id}\n💵 Số dư: ${balance} | 🎟 Vé: {tickets} (VIP: {vip}🎟) | 🎰 Vòng quay may mắn: {lucky}\n\n🌐 Trang web: Oniiai.com | 🛍️ Cửa hàng: Oniishop.us\n👥 Nhóm Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Nhóm Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Kênh Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Kênh Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Kênh Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Chào mừng đến với Onii AI Bot!\nKhám phá thế giới sáng tạo không giới hạn với các công cụ chỉnh sửa ảnh và video thông minh được hỗ trợ bởi AI.\nTùy chỉnh phong cách của bạn theo cách riêng – nhanh chóng, riêng tư và mạnh mẽ.\n\n💼 ID Tài khoản: {account_id}\n💵 Số dư: ${balance} | 🎟 Vé: {tickets} (VIP: {vip}🎟) | 🎰 Vòng quay may mắn: {lucky}\n\n🌐 Trang web: Oniiai.com | 🛍️ Cửa hàng: Oniishop.us\n👥 Nhóm Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Nhóm Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Kênh Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Kênh Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Kênh Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Thông báo quan trọng: Nếu bot bạn đang sử dụng hiện đang hiển thị là đã bị xóa hoặc vô hiệu hóa,\nvui lòng nhấp vào nút bên dưới để nhận hướng dẫn chi tiết.\n🤖 Xem danh sách bot dự phòng: @Onii1BackupBot\n🙌 Bot trao đổi video nhanh nhất thế giới – Chia sẻ để kiếm 1.5 🎟 hoặc chia sẻ không giới hạn 🎁 để nhận phần thưởng tiền mặt!\n\n🔞 Onii AI – Kênh thử nghiệm cho các công cụ chỉnh sửa ảnh và video AI Tạo nội dung người lớn phù hợp với sở thích của bạn: hình ảnh gợi cảm, video deepfake, chất lượng 4K, 100% riêng tư. ⚡️ Công nghệ độc quyền chưa được phát hành – chỉ dành cho\n\n\n🌐 Trang web: Oniiai.com | 🛍️ Cửa hàng: Oniishop.us\n👥 Nhóm Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Nhóm Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Kênh Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Kênh Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Kênh Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 ¡Bienvenido a Onii AI Bot!\nDescubre un mundo de creatividad ilimitada con nuestras herramientas inteligentes de edición de fotos y videos impulsadas por IA.\nPersonaliza tu estilo a tu manera – rápido, privado y poderoso.\n\n💼 ID de Cuenta: {account_id}\n💵 Saldo: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Giros de la suerte: {lucky}\n\n🌐 Sitio web: Oniiai.com | 🛍️ Tienda: Oniishop.us\n👥 Grupo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Grupo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canal Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canal Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canal Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 ¡Bienvenido a Onii AI Bot!\nDescubre un mundo de creatividad ilimitada con nuestras herramientas inteligentes de edición de fotos y videos impulsadas por IA.\nPersonaliza tu estilo a tu manera – rápido, privado y poderoso.\n\n💼 ID de Cuenta: {account_id}\n💵 Saldo: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Giros de la suerte: {lucky}\n\n🌐 Sitio web: Oniiai.com | 🛍️ Tienda: Oniishop.us\n👥 Grupo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Grupo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canal Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canal Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canal Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Aviso Importante: Si el bot que estás usando actualmente se muestra como eliminado o deshabilitado,\npor favor haz clic en el botón de abajo para obtener instrucciones detalladas.\n🤖 Ver la lista de bots de respaldo: @Onii1BackupBot\n🙌 El bot de intercambio de videos más rápido del mundo – ¡Comparte para ganar 1.5 🎟 o comparte sin límites 🎁 para recibir recompensas en efectivo!\n\n🔞 Onii AI – Canal Experimental para Herramientas de Edición de Fotos y Videos IA Crea contenido para adultos que coincida con tu gusto: imágenes sexys, videos deepfake, calidad 4K, 100% privado. ⚡️ Tecnología exclusiva aún no lanzada – solo para\n\n\n🌐 Sitio web: Oniiai.com | 🛍️ Tienda: Oniishop.us\n👥 Grupo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Grupo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canal Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canal Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canal Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Bienvenue sur Onii AI Bot !\nDécouvrez un monde de créativité illimitée avec nos outils intelligents d'édition de photos et vidéos alimentés par l'IA.\nPersonnalisez votre style à votre façon – rapide, privé et puissant.\n\n💼 ID du compte : {account_id}\n💵 Solde : ${balance} | 🎟 Tickets : {tickets} (VIP : {vip}🎟) | 🎰 Tours de la chance : {lucky}\n\n🌐 Site web : Oniiai.com | 🛍️ Boutique : Oniishop.us\n👥 Groupe Onii AI : t.me/+BryXTab4AA5hYWNl\n👥 Groupe Onii Shop : t.me/+dnKKXRGYm_swZTc1\n📡 Chaîne Onii AI : t.me/+DtXi9z2VgcxhYjE1\n📡 Chaîne Onii Hub : t.me/+5dQBKzTuB5UyNTI1\n📡 Chaîne Onii XXX : t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Bienvenue sur Onii AI Bot !\nDécouvrez un monde de créativité illimitée avec nos outils intelligents d'édition de photos et vidéos alimentés par l'IA.\nPersonnalisez votre style à votre façon – rapide, privé et puissant.\n\n💼 ID du compte : {account_id}\n💵 Solde : ${balance} | 🎟 Tickets : {tickets} (VIP : {vip}🎟) | 🎰 Tours de la chance : {lucky}\n\n🌐 Site web : Oniiai.com | 🛍️ Boutique : Oniishop.us\n👥 Groupe Onii AI : t.me/+BryXTab4AA5hYWNl\n👥 Groupe Onii Shop : t.me/+dnKKXRGYm_swZTc1\n📡 Chaîne Onii AI : t.me/+DtXi9z2VgcxhYjE1\n📡 Chaîne Onii Hub : t.me/+5dQBKzTuB5UyNTI1\n📡 Chaîne Onii XXX : t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Avis Important : Si le bot que vous utilisez actuellement apparaît comme supprimé ou désactivé,\nveuillez cliquer sur le bouton ci-dessous pour obtenir des instructions détaillées.\n🤖 Voir la liste des bots de sauvegarde : @Onii1BackupBot\n🙌 Le bot d'échange de vidéos le plus rapide au monde – Partagez pour gagner 1,5 🎟 ou partagez sans limites 🎁 pour recevoir des récompenses en espèces !\n\n🔞 Onii AI – Canal expérimental pour les outils d'édition de photos et vidéos IA Créez du contenu adulte qui correspond à votre goût : images sexy, vidéos deepfake, qualité 4K, 100% privé. ⚡️ Technologie exclusive pas encore publiée – uniquement pour\n\n\n🌐 Site web : Oniiai.com | 🛍️ Boutique : Oniishop.us\n👥 Groupe Onii AI : t.me/+BryXTab4AA5hYWNl\n👥 Groupe Onii Shop : t.me/+dnKKXRGYm_swZTc1\n📡 Chaîne Onii AI : t.me/+DtXi9z2VgcxhYjE1\n📡 Chaîne Onii Hub : t.me/+5dQBKzTuB5UyNTI1\n📡 Chaîne Onii XXX : t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Onii AI Bot में आपका स्वागत है!\nहमारे स्मार्ट AI-संचालित फोटो और वीडियो संपादन उपकरणों के साथ असीमित रचनात्मकता की दुनिया की खोज करें।\nअपनी शैली को अपने तरीके से अनुकूलित करें – तेज़, निजी और शक्तिशाली।\n\n💼 खाता ID: {account_id}\n💵 बैलेंस: ${balance} | 🎟 टिकट: {tickets} (VIP: {vip}🎟) | 🎰 लकी स्पिन: {lucky}\n\n🌐 वेबसाइट: Oniiai.com | 🛍️ शॉप: Oniishop.us\n👥 Onii AI ग्रुप: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop ग्रुप: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI चैनल: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub चैनल: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX चैनल: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Onii AI Bot में आपका स्वागत है!\nहमारे स्मार्ट AI-संचालित फोटो और वीडियो संपादन उपकरणों के साथ असीमित रचनात्मकता की दुनिया की खोज करें।\nअपनी शैली को अपने तरीके से अनुकूलित करें – तेज़, निजी और शक्तिशाली।\n\n💼 खाता ID: {account_id}\n💵 बैलेंस: ${balance} | 🎟 टिकट: {tickets} (VIP: {vip}🎟) | 🎰 लकी स्पिन: {lucky}\n\n🌐 वेबसाइट: Oniiai.com | 🛍️ शॉप: Oniishop.us\n👥 Onii AI ग्रुप: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop ग्रुप: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI चैनल: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub चैनल: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX चैनल: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ महत्वपूर्ण सूचना: यदि आप जो बॉट उपयोग कर रहे हैं वह वर्तमान में हटाए गए या निष्क्रिय के रूप में दिखाई दे रहा है,\nकृपया विस्तृत निर्देश प्राप्त करने के लिए नीचे दिए गए बटन पर क्लिक करें।\n🤖 बैकअप बॉट्स की सूची देखें: @Onii1BackupBot\n🙌 दुनिया का सबसे तेज़ वीडियो एक्सचेंज बॉट – 1.5 🎟 कमाने के लिए साझा करें या सीमा के बिना 🎁 साझा करके नकद पुरस्कार प्राप्त करें!\n\n🔞 Onii AI – AI फोटो और वीडियो संपादन उपकरणों के लिए प्रयोगात्मक चैनल आपकी पसंद के अनुसार वयस्क सामग्री बनाएं: सेक्सी चित्र, डीपफेक वीडियो, 4K गुणवत्ता, 100% निजी। ⚡️ विशेष तकनीक अभी तक जारी नहीं की गई – केवल\n\n\n🌐 वेबसाइट: Oniiai.com | 🛍️ शॉप: Oniishop.us\n👥 Onii AI ग्रुप: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop ग्रुप: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI चैनल: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub चैनल: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX चैनल: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Onii AI Bot වෙත සාදරයෙන් පිළිගනිමු!\nඅපගේ ස්මාර්ට් AI-බලය ලත් ඡායාරූප සහ වීඩියෝ සංස්කරණ මෙවලම් සමඟ අසීමිත නිර්මාණශීලීත්වයේ ලෝකයක් සොයා ගන්න.\nඔබේම ආකාරයට ඔබේ ශෛලිය අභිරුචිකරණය කරන්න – වේගවත්, පුද්ගලික සහ බලවත්.\n\n💼 ගණක අංකය: {account_id}\n💵 ශේෂය: ${balance} | 🎟 ටිකට්: {tickets} (VIP: {vip}🎟) | 🎰 අහඹු භ්‍රමණ: {lucky}\n\n🌐 වෙබ් අඩවිය: Oniiai.com | 🛍️ වෙළඳසැල: Oniishop.us\n👥 Onii AI කණ්ඩායම: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop කණ්ඩායම: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI නාලිකාව: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub නාලිකාව: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX නාලිකාව: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Onii AI Bot වෙත සාදරයෙන් පිළිගනිමු!\nඅපගේ ස්මාර්ට් AI-බලය ලත් ඡායාරූප සහ වීඩියෝ සංස්කරණ මෙවලම් සමඟ අසීමිත නිර්මාණශීලීත්වයේ ලෝකයක් සොයා ගන්න.\nඔබේම ආකාරයට ඔබේ ශෛලිය අභිරුචිකරණය කරන්න – වේගවත්, පුද්ගලික සහ බලවත්.\n\n💼 ගණක අංකය: {account_id}\n💵 ශේෂය: ${balance} | 🎟 ටිකට්: {tickets} (VIP: {vip}🎟) | 🎰 අහඹු භ්‍රමණ: {lucky}\n\n🌐 වෙබ් අඩවිය: Oniiai.com | 🛍️ වෙළඳසැල: Oniishop.us\n👥 Onii AI කණ්ඩායම: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop කණ්ඩායම: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI නාලිකාව: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub නාලිකාව: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX නාලිකාව: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ වැදගත් දැනුම්දීම: ඔබ භාවිතා කරන bot අද වන විට මකා දමා ඇති හෝ අක්‍රිය කර ඇති ලෙස පෙන්වන්නේ නම්,\nකරුණාකර විස්තරාත්මක උපදෙස් ලබා ගැනීමට පහත බොත්තම ක්ලික් කරන්න.\n🤖 උපකාරක bot ලැයිස්තුව බලන්න: @Onii1BackupBot\n🙌 ලෝකයේ වේගවත්ම වීඩියෝ හුවමාරු bot – 1.5 🎟 උපයා ගැනීමට හුවමාරු කරන්න හෝ සීමා නැතිව 🎁 හුවමාරු කර ධන ප්‍රතිලාභ ලබා ගන්න!\n\n🔞 Onii AI – AI ඡායාරූප සහ වීඩියෝ සංස්කරණ මෙවලම් සඳහා පර්යේෂණාත්මක නාලිකාව ඔබේ රසයට ගැලපෙන ප්‍රතිපත්ති අන්තර්ගතය සාදන්න: ලිංගික රූප, deepfake වීඩියෝ, 4K ගුණාත්මක, 100% පුද්ගලික. ⚡️ තවම මුදා නොහරින එක් එක් තාක්ෂණය – ඇතුළුව\n\n\n🌐 වෙබ් අඩවිය: Oniiai.com | 🛍️ වෙළඳසැල: Oniishop.us\n👥 Onii AI කණ්ඩායම: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop කණ්ඩායම: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI නාලිකාව: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub නාලිකාව: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX නාලිකාව: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Willkommen bei Onii AI Bot!\nEntdecken Sie eine Welt unbegrenzter Kreativität mit unseren intelligenten KI-gestützten Foto- und Video-Bearbeitungstools.\nPassen Sie Ihren Stil nach Ihren Wünschen an – schnell, privat und leistungsstark.\n\n💼 Konto-ID: {account_id}\n💵 Guthaben: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Glücksspins: {lucky}\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Onii AI Gruppe: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Gruppe: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanal: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanal: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanal: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Willkommen bei Onii AI Bot!\nEntdecken Sie eine Welt unbegrenzter Kreativität mit unseren intelligenten KI-gestützten Foto- und Video-Bearbeitungstools.\nPassen Sie Ihren Stil nach Ihren Wünschen an – schnell, privat und leistungsstark.\n\n💼 Konto-ID: {account_id}\n💵 Guthaben: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Glücksspins: {lucky}\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Onii AI Gruppe: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Gruppe: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanal: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanal: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanal: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Wichtiger Hinweis: Wenn der Bot, den Sie verwenden, derzeit als gelöscht oder deaktiviert angezeigt wird,\nbitte klicken Sie auf die Schaltfläche unten, um detaillierte Anweisungen zu erhalten.\n🤖 Liste der Backup-Bots anzeigen: @Onii1BackupBot\n🙌 Der schnellste Video-Austausch-Bot der Welt – Teilen Sie, um 1,5 🎟 zu verdienen oder teilen Sie ohne Grenzen 🎁, um Bargeld-Belohnungen zu erhalten!\n\n🔞 Onii AI – Experimenteller Kanal für KI-Foto- und Video-Bearbeitungstools Erstellen Sie Erwachseneninhalte, die Ihrem Geschmack entsprechen: sexy Bilder, Deepfake-Videos, 4K-Qualität, 100% privat. ⚡️ Exklusive Technologie, noch nicht veröffentlicht – nur für\n\n\n🌐 Website: Oniiai.com | 🛍️ Shop: Oniishop.us\n👥 Onii AI Gruppe: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Gruppe: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanal: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanal: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanal: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 欢迎来到 Onii AI Bot！\n通过我们智能AI驱动的照片和视频编辑工具，发现无限创意的世界。\n按照您的方式定制您的风格——快速、私密且强大。\n\n💼 账户ID：{account_id}\n💵 余额：${balance} | 🎟 票券：{tickets} (VIP：{vip}🎟) | 🎰 幸运转盘：{lucky}\n\n🌐 网站：Oniiai.com | 🛍️ 商店：Oniishop.us\n👥 Onii AI 群组：t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop 群组：t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI 频道：t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub 频道：t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX 频道：t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 欢迎来到 Onii AI Bot！\n通过我们智能AI驱动的照片和视频编辑工具，发现无限创意的世界。\n按照您的方式定制您的风格——快速、私密且强大。\n\n💼 账户ID：{account_id}\n💵 余额：${balance} | 🎟 票券：{tickets} (VIP：{vip}🎟) | 🎰 幸运转盘：{lucky}\n\n🌐 网站：Oniiai.com | 🛍️ 商店：Oniishop.us\n👥 Onii AI 群组：t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop 群组：t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI 频道：t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub 频道：t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX 频道：t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ 重要通知：如果您当前使用的机器人显示为已删除或已禁用，\n请点击下方按钮获取详细说明。\n🤖 查看备用机器人列表：@Onii1BackupBot\n🙌 世界最快的视频交换机器人——分享赚取1.5🎟或无限分享🎁获得现金奖励！\n\n🔞 Onii AI – AI照片和视频编辑删除工具的实验频道 创建符合您品味的成人内容：性感图片、深度伪造视频、4K质量、100%私密。⚡️独家技术尚未发布——仅限\n\n\n🌐 网站：Oniiai.com | 🛍️ 商店：Oniishop.us\n👥 Onii AI 群组：t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop 群组：t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI 频道：t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub 频道：t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX 频道：t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Добро пожаловать в Onii AI Bot!\nОткройте мир безграничного творчества с нашими умными инструментами для редактирования фото и видео на основе ИИ.\nНастройте свой стиль по-своему – быстро, приватно и мощно.\n\n💼 ID аккаунта: {account_id}\n💵 Баланс: ${balance} | 🎟 Билеты: {tickets} (VIP: {vip}🎟) | 🎰 Удачные спины: {lucky}\n\n🌐 Сайт: Oniiai.com | 🛍️ Магазин: Oniishop.us\n👥 Группа Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Группа Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Канал Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Канал Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Канал Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Добро пожаловать в Onii AI Bot!\nОткройте мир безграничного творчества с нашими умными инструментами для редактирования фото и видео на основе ИИ.\nНастройте свой стиль по-своему – быстро, приватно и мощно.\n\n💼 ID аккаунта: {account_id}\n💵 Баланс: ${balance} | 🎟 Билеты: {tickets} (VIP: {vip}🎟) | 🎰 Удачные спины: {lucky}\n\n🌐 Сайт: Oniiai.com | 🛍️ Магазин: Oniishop.us\n👥 Группа Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Группа Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Канал Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Канал Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Канал Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Важное уведомление: Если бот, который вы используете, в настоящее время отображается как удаленный или отключенный,\nпожалуйста, нажмите кнопку ниже, чтобы получить подробные инструкции.\n🤖 Посмотреть список резервных ботов: @Onii1BackupBot\n🙌 Самый быстрый бот обмена видео в мире – делитесь, чтобы заработать 1,5 🎟 или делитесь без ограничений 🎁, чтобы получить денежные вознаграждения!\n\n🔞 Onii AI – Экспериментальный канал для инструментов редактирования фото и видео ИИ Создавайте контент для взрослых, соответствующий вашему вкусу: сексуальные изображения, дипфейк видео, качество 4K, 100% приватно. ⚡️ Эксклюзивная технология еще не выпущена – только для\n\n\n🌐 Сайт: Oniiai.com | 🛍️ Магазин: Oniishop.us\n👥 Группа Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Группа Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Канал Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Канал Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Канал Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 مرحباً بك في Onii AI Bot!\nاكتشف عالمًا من الإبداع اللامحدود مع أدوات التحرير الذكية للصور والفيديو المدعومة بالذكاء الاصطناعي.\nخصص أسلوبك بطريقتك – سريع وخاص وقوي.\n\n💼 معرف الحساب: {account_id}\n💵 الرصيد: ${balance} | 🎟 التذاكر: {tickets} (VIP: {vip}🎟) | 🎰 الدورات المحظوظة: {lucky}\n\n🌐 الموقع: Oniiai.com | 🛍️ المتجر: Oniishop.us\n👥 مجموعة Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 مجموعة Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 قناة Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 قناة Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 قناة Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 مرحباً بك في Onii AI Bot!\nاكتشف عالمًا من الإبداع اللامحدود مع أدوات التحرير الذكية للصور والفيديو المدعومة بالذكاء الاصطناعي.\nخصص أسلوبك بطريقتك – سريع وخاص وقوي.\n\n💼 معرف الحساب: {account_id}\n💵 الرصيد: ${balance} | 🎟 التذاكر: {tickets} (VIP: {vip}🎟) | 🎰 الدورات المحظوظة: {lucky}\n\n🌐 الموقع: Oniiai.com | 🛍️ المتجر: Oniishop.us\n👥 مجموعة Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 مجموعة Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 قناة Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 قناة Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 قناة Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ إشعار مهم: إذا كان البوت الذي تستخدمه يظهر حالياً كمحذوف أو معطل،\nيرجى النقر على الزر أدناه للحصول على تعليمات مفصلة.\n🤖 عرض قائمة البوتات الاحتياطية: @Onii1BackupBot\n🙌 أسرع بوت تبادل فيديو في العالم – شارك لكسب 1.5 🎟 أو شارك بلا حدود 🎁 للحصول على مكافآت نقدية!\n\n🔞 Onii AI – قناة تجريبية لأدوات تحرير الصور والفيديو بالذكاء الاصطناعي إنشاء محتوى للبالغين يناسب ذوقك: صور مثيرة، فيديوهات مزيفة عميقة، جودة 4K، 100% خاص. ⚡️ تقنية حصرية لم يتم إصدارها بعد – فقط لـ\n\n\n🌐 الموقع: Oniiai.com | 🛍️ المتجر: Oniishop.us\n👥 مجموعة Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 مجموعة Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 قناة Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 قناة Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 قناة Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Bem-vindo ao Onii AI Bot!\nDescubra um mundo de criatividade ilimitada com nossas ferramentas inteligentes de edição de fotos e vídeos alimentadas por IA.\nPersonalize seu estilo à sua maneira – rápido, privado e poderoso.\n\n💼 ID da Conta: {account_id}\n💵 Saldo: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Giros da Sorte: {lucky}\n\n🌐 Site: Oniiai.com | 🛍️ Loja: Oniishop.us\n👥 Grupo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Grupo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canal Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canal Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canal Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Bem-vindo ao Onii AI Bot!\nDescubra um mundo de criatividade ilimitada com nossas ferramentas inteligentes de edição de fotos e vídeos alimentadas por IA.\nPersonalize seu estilo à sua maneira – rápido, privado e poderoso.\n\n💼 ID da Conta: {account_id}\n💵 Saldo: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Giros da Sorte: {lucky}\n\n🌐 Site: Oniiai.com | 🛍️ Loja: Oniishop.us\n👥 Grupo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Grupo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canal Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canal Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canal Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Aviso Importante: Se o bot que você está usando atualmente aparece como excluído ou desativado,\nclique no botão abaixo para obter instruções detalhadas.\n🤖 Ver lista de bots de backup: @Onii1BackupBot\n🙌 O bot de troca de vídeo mais rápido do mundo – Compartilhe para ganhar 1,5 🎟 ou compartilhe sem limites 🎁 para receber recompensas em dinheiro!\n\n🔞 Onii AI – Canal Experimental para Ferramentas de Edição de Fotos e Vídeos IA Crie conteúdo adulto que corresponda ao seu gosto: imagens sensuais, vídeos deepfake, qualidade 4K, 100% privado. ⚡️ Tecnologia exclusiva ainda não lançada – apenas para\n\n\n🌐 Site: Oniiai.com | 🛍️ Loja: Oniishop.us\n👥 Grupo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Grupo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canal Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canal Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canal Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Benvenuto in Onii AI Bot!\nScopri un mondo di creatività illimitata con i nostri strumenti intelligenti di editing di foto e video alimentati dall'IA.\nPersonalizza il tuo stile a modo tuo – veloce, privato e potente.\n\n💼 ID Account: {account_id}\n💵 Saldo: ${balance} | 🎟 Biglietti: {tickets} (VIP: {vip}🎟) | 🎰 Giri Fortunati: {lucky}\n\n🌐 Sito Web: Oniiai.com | 🛍️ Negozio: Oniishop.us\n👥 Gruppo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Gruppo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canale Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canale Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canale Onii XXX: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Benvenuto in Onii AI Bot!\nScopri un mondo di creatività illimitata con i nostri strumenti intelligenti di editing di foto e video alimentati dall'IA.\nPersonalizza il tuo stile a modo tuo – veloce, privato e potente.\n\n💼 ID Account: {account_id}\n💵 Saldo: ${balance} | 🎟 Biglietti: {tickets} (VIP: {vip}🎟) | 🎰 Giri Fortunati: {lucky}\n\n🌐 Sito Web: Oniiai.com | 🛍️ Negozio: Oniishop.us\n👥 Gruppo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Gruppo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canale Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canale Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canale Onii XXX: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Avviso Importante: Se il bot che stai utilizzando attualmente appare come eliminato o disabilitato,\nclicca sul pulsante qui sotto per ottenere istruzioni dettagliate.\n🤖 Visualizza elenco bot di backup: @Onii1BackupBot\n🙌 Il bot di scambio video più veloce al mondo – Condividi per guadagnare 1,5 🎟 o condividi senza limiti 🎁 per ricevere ricompense in denaro!\n\n🔞 Onii AI – Canale Sperimentale per Strumenti di Editing Foto e Video IA Crea contenuti per adulti che corrispondono ai tuoi gusti: immagini sexy, video deepfake, qualità 4K, 100% privato. ⚡️ Tecnologia esclusiva non ancora rilasciata – solo per\n\n\n🌐 Sito Web: Oniiai.com | 🛍️ Negozio: Oniishop.us\n👥 Gruppo Onii AI: t.me/+BryXTab4AA5hYWNl\n👥 Gruppo Onii Shop: t.me/+dnKKXRGYm_swZTc1\n📡 Canale Onii AI: t.me/+DtXi9z2VgcxhYjE1\n📡 Canale Onii Hub: t.me/+5dQBKzTuB5UyNTI1\n📡 Canale Onii XXX: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Onii AI Botへようこそ！\n私たちのスマートAI搭載の写真・動画編集ツールで、無限の創造性の世界を発見してください。\nあなたの方法でスタイルをカスタマイズ – 高速、プライベート、そして強力。\n\n💼 アカウントID：{account_id}\n💵 残高：${balance} | 🎟 チケット：{tickets} (VIP：{vip}🎟) | 🎰 ラッキースピン：{lucky}\n\n🌐 ウェブサイト：Oniiai.com | 🛍️ ショップ：Oniishop.us\n👥 Onii AIグループ：t.me/+BryXTab4AA5hYWNl\n👥 Onii Shopグループ：t.me/+dnKKXRGYm_swZTc1\n📡 Onii AIチャンネル：t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hubチャンネル：t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXXチャンネル：t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Onii AI Botへようこそ！\n私たちのスマートAI搭載の写真・動画編集ツールで、無限の創造性の世界を発見してください。\nあなたの方法でスタイルをカスタマイズ – 高速、プライベート、そして強力。\n\n💼 アカウントID：{account_id}\n💵 残高：${balance} | 🎟 チケット：{tickets} (VIP：{vip}🎟) | 🎰 ラッキースピン：{lucky}\n\n🌐 ウェブサイト：Oniiai.com | 🛍️ ショップ：Oniishop.us\n👥 Onii AIグループ：t.me/+BryXTab4AA5hYWNl\n👥 Onii Shopグループ：t.me/+dnKKXRGYm_swZTc1\n📡 Onii AIチャンネル：t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hubチャンネル：t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXXチャンネル：t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ 重要なお知らせ：現在使用しているボットが削除済みまたは無効として表示されている場合、\n詳細な手順を取得するには、下のボタンをクリックしてください。\n🤖 バックアップボットのリストを表示：@Onii1BackupBot\n🙌 世界最速の動画交換ボット – 1.5🎟を獲得するためにシェア、または制限なしで🎁シェアして現金報酬を受け取ろう！\n\n🔞 Onii AI – AI写真・動画編集ツールの実験チャンネル あなたの好みに合ったアダルトコンテンツを作成：セクシーな画像、ディープフェイク動画、4K品質、100%プライベート。⚡️まだリリースされていない独占技術 – 対象者限定\n\n\n🌐 ウェブサイト：Oniiai.com | 🛍️ ショップ：Oniishop.us\n👥 Onii AIグループ：t.me/+BryXTab4AA5hYWNl\n👥 Onii Shopグループ：t.me/+dnKKXRGYm_swZTc1\n📡 Onii AIチャンネル：t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hubチャンネル：t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXXチャンネル：t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Onii AI Bot에 오신 것을 환영합니다!\n우리의 스마트 AI 기반 사진 및 비디오 편집 도구로 무한한 창의성의 세계를 발견하세요.\n당신만의 방식으로 스타일을 맞춤화하세요 – 빠르고, 비공개이며, 강력합니다.\n\n💼 계정 ID: {account_id}\n💵 잔액: ${balance} | 🎟 티켓: {tickets} (VIP: {vip}🎟) | 🎰 럭키 스핀: {lucky}\n\n🌐 웹사이트: Oniiai.com | 🛍️ 쇼핑몰: Oniishop.us\n👥 Onii AI 그룹: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop 그룹: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI 채널: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub 채널: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX 채널: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Onii AI Bot에 오신 것을 환영합니다!\n우리의 스마트 AI 기반 사진 및 비디오 편집 도구로 무한한 창의성의 세계를 발견하세요.\n당신만의 방식으로 스타일을 맞춤화하세요 – 빠르고, 비공개이며, 강력합니다.\n\n💼 계정 ID: {account_id}\n💵 잔액: ${balance} | 🎟 티켓: {tickets} (VIP: {vip}🎟) | 🎰 럭키 스핀: {lucky}\n\n🌐 웹사이트: Oniiai.com | 🛍️ 쇼핑몰: Oniishop.us\n👥 Onii AI 그룹: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop 그룹: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI 채널: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub 채널: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX 채널: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ 중요 공지: 현재 사용하고 있는 봇이 삭제되었거나 비활성화된 것으로 표시되는 경우,\n자세한 지침을 받으려면 아래 버튼을 클릭하세요.\n🤖 백업 봇 목록 보기: @Onii1BackupBot\n🙌 세계에서 가장 빠른 비디오 교환 봇 – 1.5🎟을 획득하기 위해 공유하거나 제한 없이 🎁공유하여 현금 보상을 받으세요!\n\n🔞 Onii AI – AI 사진 및 비디오 편집 도구를 위한 실험적 채널 당신의 취향에 맞는 성인 콘텐츠를 만드세요: 섹시한 이미지, 딥페이크 비디오, 4K 품질, 100% 비공개. ⚡️ 아직 출시되지 않은 독점 기술 – 대상자만\n\n\n🌐 웹사이트: Oniiai.com | 🛍️ 쇼핑몰: Oniishop.us\n👥 Onii AI 그룹: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop 그룹: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI 채널: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub 채널: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX 채널: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Onii AI Bot'a hoş geldiniz!\nAkıllı AI destekli fotoğraf ve video düzenleme araçlarımızla sınırsız yaratıcılık dünyasını keşfedin.\nStilinizi kendi tarzınızda özelleştirin – hızlı, özel ve güçlü.\n\n💼 Hesap ID: {account_id}\n💵 Bakiye: ${balance} | 🎟 Bilet: {tickets} (VIP: {vip}🎟) | 🎰 Şanslı Çarklar: {lucky}\n\n🌐 Web Sitesi: Oniiai.com | 🛍️ Mağaza: Oniishop.us\n👥 Onii AI Grubu: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Grubu: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanalı: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanalı: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanalı: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Onii AI Bot'a hoş geldiniz!\nAkıllı AI destekli fotoğraf ve video düzenleme araçlarımızla sınırsız yaratıcılık dünyasını keşfedin.\nStilinizi kendi tarzınızda özelleştirin – hızlı, özel ve güçlü.\n\n💼 Hesap ID: {account_id}\n💵 Bakiye: ${balance} | 🎟 Bilet: {tickets} (VIP: {vip}🎟) | 🎰 Şanslı Çarklar: {lucky}\n\n🌐 Web Sitesi: Oniiai.com | 🛍️ Mağaza: Oniishop.us\n👥 Onii AI Grubu: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Grubu: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanalı: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanalı: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanalı: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Önemli Duyuru: Kullandığınız bot şu anda silinmiş veya devre dışı olarak görünüyorsa,\nlütfen ayrıntılı talimatlar almak için aşağıdaki düğmeye tıklayın.\n🤖 Yedek bot listesini görüntüle: @Onii1BackupBot\n🙌 Dünyanın en hızlı video değişim botu – 1.5🎟 kazanmak için paylaşın veya sınırsız 🎁paylaşarak nakit ödüller alın!\n\n🔞 Onii AI – AI Fotoğraf ve Video Düzenleme Araçları için Deneysel Kanal Zevkinize uygun yetişkin içeriği oluşturun: seksi görüntüler, deepfake videolar, 4K kalite, %100 özel. ⚡️ Henüz yayınlanmamış özel teknoloji – sadece\n\n\n🌐 Web Sitesi: Oniiai.com | 🛍️ Mağaza: Oniishop.us\n👥 Onii AI Grubu: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Grubu: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanalı: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanalı: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanalı: t.me/+pHElu4SCq_NhMmFl"
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
            "new": "🙌 Welkom bij Onii AI Bot!\nOntdek een wereld van onbeperkte creativiteit met onze slimme AI-aangedreven foto- en video-editing tools.\nPas je stijl aan op jouw manier – snel, privé en krachtig.\n\n💼 Account ID: {account_id}\n💵 Saldo: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Geluksspins: {lucky}\n\n🌐 Website: Oniiai.com | 🛍️ Winkel: Oniishop.us\n👥 Onii AI Groep: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Groep: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanaal: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanaal: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanaal: t.me/+pHElu4SCq_NhMmFl",
            "back": "🙌 Welkom bij Onii AI Bot!\nOntdek een wereld van onbeperkte creativiteit met onze slimme AI-aangedreven foto- en video-editing tools.\nPas je stijl aan op jouw manier – snel, privé en krachtig.\n\n💼 Account ID: {account_id}\n💵 Saldo: ${balance} | 🎟 Tickets: {tickets} (VIP: {vip}🎟) | 🎰 Geluksspins: {lucky}\n\n🌐 Website: Oniiai.com | 🛍️ Winkel: Oniishop.us\n👥 Onii AI Groep: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Groep: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanaal: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanaal: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanaal: t.me/+pHElu4SCq_NhMmFl"
        },
        "important_notice": {
            "text": "⚠️ Belangrijke Mededeling: Als de bot die u gebruikt momenteel wordt weergegeven als verwijderd of uitgeschakeld,\nklik op de knop hieronder voor gedetailleerde instructies.\n🤖 Bekijk lijst van back-up bots: @Onii1BackupBot\n🙌 's Werelds snelste video-uitwisselingsbot – Deel om 1,5🎟 te verdienen of deel zonder limieten 🎁 om geldprijzen te ontvangen!\n\n🔞 Onii AI – Experimenteel Kanaal voor AI Foto- en Video-editing Tools Maak volwassen inhoud die bij uw smaak past: sexy afbeeldingen, deepfake video's, 4K kwaliteit, 100% privé. ⚡️ Exclusieve technologie nog niet uitgebracht – alleen voor\n\n\n🌐 Website: Oniiai.com | 🛍️ Winkel: Oniishop.us\n👥 Onii AI Groep: t.me/+BryXTab4AA5hYWNl\n👥 Onii Shop Groep: t.me/+dnKKXRGYm_swZTc1\n📡 Onii AI Kanaal: t.me/+DtXi9z2VgcxhYjE1\n📡 Onii Hub Kanaal: t.me/+5dQBKzTuB5UyNTI1\n📡 Onii XXX Kanaal: t.me/+pHElu4SCq_NhMmFl"
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
