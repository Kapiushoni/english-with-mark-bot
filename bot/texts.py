"""Все тексты бота на двух языках. Меняй здесь — код трогать не нужно."""

TEXTS: dict[str, dict[str, str]] = {
    "choose_lang": {
        "uk": "Оберіть мову / Choose your language",
        "en": "Оберіть мову / Choose your language",
    },
    "welcome": {
        "uk": (
            "👋 Привіт, {name}!\n\n"
            "Це бот курсу <b>English with Mark</b> — розмовна англійська без зубріння.\n\n"
            "Тут можна оформити доступ до закритого каналу з уроками, переглянути свою підписку "
            "і зв'язатися з підтримкою."
        ),
        "en": (
            "👋 Hi, {name}!\n\n"
            "This is the <b>English with Mark</b> course bot — spoken English without cramming.\n\n"
            "Here you can get access to the private lessons channel, check your subscription "
            "and contact support."
        ),
    },
    "btn_tariffs": {"uk": "💎 Тарифи", "en": "💎 Plans"},
    "btn_my_sub": {"uk": "👤 Моя підписка", "en": "👤 My subscription"},
    "btn_about": {"uk": "📚 Про курс", "en": "📚 About the course"},
    "btn_support": {"uk": "💬 Підтримка", "en": "💬 Support"},
    "btn_lang": {"uk": "🌐 Мова", "en": "🌐 Language"},
    "btn_back": {"uk": "← Назад", "en": "← Back"},
    "btn_renew": {"uk": "🔄 Продовжити", "en": "🔄 Renew"},
    "btn_get_link": {"uk": "🔗 Отримати посилання", "en": "🔗 Get invite link"},
    "about": {
        "uk": (
            "<b>English with Mark</b>\n\n"
            "• 3 нових відеоуроки щотижня\n"
            "• Живий ефір із розбором помилок щонеділі\n"
            "• Домашні завдання з перевіркою\n"
            "• Спільнота учнів для практики\n\n"
            "Рівень: від A2 до B2. Доступ відкривається одразу після оплати."
        ),
        "en": (
            "<b>English with Mark</b>\n\n"
            "• 3 new video lessons every week\n"
            "• Live session with mistake review every Sunday\n"
            "• Homework with feedback\n"
            "• A community of learners to practise with\n\n"
            "Level: A2 to B2. Access opens right after payment."
        ),
    },
    "tariffs_header": {
        "uk": "Оберіть тариф. Оплата в Telegram Stars ⭐ — прямо в Telegram, без карток і сайтів.",
        "en": "Choose a plan. Pay with Telegram Stars ⭐ — right inside Telegram, no cards or websites.",
    },
    "tariff_button": {"uk": "{title} — {stars} ⭐", "en": "{title} — {stars} ⭐"},
    "sub_active": {
        "uk": "✅ Підписка активна до <b>{date}</b> (UTC).\nТариф: {tariff}",
        "en": "✅ Your subscription is active until <b>{date}</b> (UTC).\nPlan: {tariff}",
    },
    "sub_lifetime": {
        "uk": "✅ У вас доступ назавжди. Дякуємо, що ви з нами!",
        "en": "✅ You have lifetime access. Thank you for being with us!",
    },
    "sub_none": {
        "uk": "У вас поки немає активної підписки. Оберіть тариф, щоб отримати доступ.",
        "en": "You don't have an active subscription yet. Choose a plan to get access.",
    },
    "already_lifetime": {
        "uk": "У вас уже є доступ назавжди — платити більше не потрібно 🙂",
        "en": "You already have lifetime access — no need to pay again 🙂",
    },
    "paid_success": {
        "uk": (
            "🎉 Оплату отримано, дякуємо!\n\n{status}\n\n"
            "Ваше особисте посилання на канал (одноразове, діє 24 години):\n{link}"
        ),
        "en": (
            "🎉 Payment received, thank you!\n\n{status}\n\n"
            "Your personal channel link (single-use, valid for 24 hours):\n{link}"
        ),
    },
    "invite_link": {
        "uk": "Ваше нове посилання на канал (одноразове, діє 24 години):\n{link}",
        "en": "Your new channel link (single-use, valid for 24 hours):\n{link}",
    },
    "invite_error": {
        "uk": "Не вдалося створити посилання. Ми вже отримали сповіщення і скоро надішлемо його вручну.",
        "en": "Couldn't create the link. We've been notified and will send it to you manually soon.",
    },
    "payment_error": {
        "uk": "Цей рахунок більше не дійсний. Відкрийте тарифи і спробуйте ще раз.",
        "en": "This invoice is no longer valid. Open the plans and try again.",
    },
    "support": {
        "uk": "Питання щодо курсу чи оплати? Пишіть: @{support}\nВідповідаємо протягом дня.",
        "en": "Questions about the course or payment? Message us: @{support}\nWe reply within a day.",
    },
    "paysupport": {
        "uk": (
            "Підтримка з оплат: @{support}\n"
            "Вкажіть дату оплати і тариф. Підтримка Telegram не може допомогти з покупками в цьому боті."
        ),
        "en": (
            "Payment support: @{support}\n"
            "Include the payment date and plan. Telegram support can't help with purchases made in this bot."
        ),
    },
    "terms": {
        "uk": (
            "<b>Умови</b>\n\n"
            "• Оплата відкриває доступ до закритого каналу на обраний термін.\n"
            "• Після закінчення терміну доступ закривається автоматично.\n"
            "• Повернення можливе протягом 3 днів після оплати — пишіть у /paysupport."
        ),
        "en": (
            "<b>Terms</b>\n\n"
            "• Payment grants access to the private channel for the selected period.\n"
            "• Access is closed automatically when the period ends.\n"
            "• Refunds are possible within 3 days of payment — contact /paysupport."
        ),
    },
    "reminder_3d": {
        "uk": "⏰ Ваша підписка закінчується через 3 дні ({date} UTC). Продовжіть, щоб не втратити доступ.",
        "en": "⏰ Your subscription ends in 3 days ({date} UTC). Renew to keep your access.",
    },
    "reminder_1d": {
        "uk": "⚠️ Завтра ({date} UTC) доступ до каналу закриється. Продовжіть підписку зараз.",
        "en": "⚠️ Your channel access closes tomorrow ({date} UTC). Renew your subscription now.",
    },
    "expired": {
        "uk": "Термін підписки закінчився, доступ до каналу закрито. Повертайтеся будь-коли 👇",
        "en": "Your subscription has ended and channel access is closed. Come back any time 👇",
    },
    "granted": {
        "uk": "🎁 Вам відкрито доступ до курсу!\n\n{status}\n\nПосилання на канал (одноразове, 24 години):\n{link}",
        "en": "🎁 You've been granted access to the course!\n\n{status}\n\nChannel link (single-use, 24 hours):\n{link}",
    },
    "refunded": {
        "uk": "Кошти повернено, доступ до каналу закрито.",
        "en": "Your payment has been refunded and channel access is closed.",
    },
    "your_id": {"uk": "Ваш Telegram ID: <code>{id}</code>", "en": "Your Telegram ID: <code>{id}</code>"},
}


def t(lang: str, key: str, **kwargs: object) -> str:
    lang = lang if lang in ("uk", "en") else "uk"
    text = TEXTS[key][lang]
    return text.format(**kwargs) if kwargs else text
