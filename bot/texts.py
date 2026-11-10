"""All bot texts in two languages (uk, en). Edit them here, no code changes needed."""

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
    # Language picker buttons
    "btn_lang_uk": {"uk": "🇺🇦 Українська", "en": "🇺🇦 Українська"},
    "btn_lang_en": {"uk": "🇬🇧 English", "en": "🇬🇧 English"},
    # Bot command descriptions (Telegram command menu)
    "cmd_start": {"uk": "Головне меню", "en": "Main menu"},
    "cmd_menu": {"uk": "Меню", "en": "Menu"},
    "cmd_terms": {"uk": "Умови", "en": "Terms"},
    "cmd_paysupport": {"uk": "Підтримка з оплат", "en": "Payment support"},
    "gift_access": {"uk": "Подарунковий доступ", "en": "Gift access"},
    # --- Admin texts (shown in the language the admin picked in the bot) ---
    "admin_help": {
        "uk": (
            "<b>Адмін-панель</b>\n\n"
            "/stats — статистика\n"
            "/grant <code>user_id днів</code> — видати доступ (наприклад <code>/grant 123456 30</code>, "
            "<code>/grant 123456 life</code> — назавжди)\n"
            "/revoke <code>user_id</code> — закрити доступ\n"
            "/refund <code>user_id</code> — повернути зірки за останню оплату й закрити доступ\n"
            "/broadcast <code>текст</code> — розсилка всім користувачам бота\n\n"
            "Перешліть сюди будь-який пост із каналу — бот покаже його ID."
        ),
        "en": (
            "<b>Admin panel</b>\n\n"
            "/stats — statistics\n"
            "/grant <code>user_id days</code> — grant access (e.g. <code>/grant 123456 30</code>, "
            "<code>/grant 123456 life</code> — lifetime)\n"
            "/revoke <code>user_id</code> — revoke access\n"
            "/refund <code>user_id</code> — refund the last payment in Stars and revoke access\n"
            "/broadcast <code>text</code> — message all bot users\n\n"
            "Forward any post from the channel here and the bot will show its ID."
        ),
    },
    "admin_stats": {
        "uk": (
            "<b>Статистика</b>\n\n"
            "Користувачів: {users} (заблокували бота: {blocked})\n"
            "Активних підписок: {active}\n"
            "Оплат: {payments}\n"
            "Виручка: {revenue} ⭐"
        ),
        "en": (
            "<b>Statistics</b>\n\n"
            "Users: {users} (blocked the bot: {blocked})\n"
            "Active subscriptions: {active}\n"
            "Payments: {payments}\n"
            "Revenue: {revenue} ⭐"
        ),
    },
    "grant_usage": {
        "uk": "Формат: <code>/grant user_id днів</code> або <code>/grant user_id life</code>",
        "en": "Usage: <code>/grant user_id days</code> or <code>/grant user_id life</code>",
    },
    "grant_bad_args": {
        "uk": "user_id і кількість днів мають бути числами (або life).",
        "en": "user_id and days must be numbers (or life).",
    },
    "user_not_found": {
        "uk": "Цей користувач ще не запускав бота. Попросіть його натиснути /start.",
        "en": "This user hasn't started the bot yet. Ask them to press /start.",
    },
    "grant_link_failed": {
        "uk": "Доступ видано, але посилання не створилося: {error}",
        "en": "Access granted, but the invite link couldn't be created: {error}",
    },
    "grant_done": {"uk": "✅ Доступ видано. {status}", "en": "✅ Access granted. {status}"},
    "not_delivered": {"uk": "⚠️ Повідомлення не доставлено.", "en": "⚠️ The message wasn't delivered."},
    "revoke_usage": {"uk": "Формат: <code>/revoke user_id</code>", "en": "Usage: <code>/revoke user_id</code>"},
    "no_subscription": {"uk": "У користувача немає підписки.", "en": "This user has no subscription."},
    "revoked": {"uk": "✅ Доступ закрито.", "en": "✅ Access revoked."},
    "refund_usage": {"uk": "Формат: <code>/refund user_id</code>", "en": "Usage: <code>/refund user_id</code>"},
    "refund_not_found": {"uk": "Не знайдено оплат для повернення.", "en": "No payments found to refund."},
    "refund_rejected": {"uk": "Telegram відхилив повернення: {error}", "en": "Telegram rejected the refund: {error}"},
    "refund_done": {
        "uk": "✅ Повернено {amount} ⭐, доступ закрито.",
        "en": "✅ Refunded {amount} ⭐, access revoked.",
    },
    "broadcast_usage": {
        "uk": "Формат: <code>/broadcast текст повідомлення</code>",
        "en": "Usage: <code>/broadcast message text</code>",
    },
    "broadcast_start": {
        "uk": "Починаю розсилку на {count} користувачів…",
        "en": "Starting broadcast to {count} users…",
    },
    "broadcast_done": {
        "uk": "✅ Розсилку завершено: доставлено {sent} з {total}.",
        "en": "✅ Broadcast finished: delivered {sent} of {total}.",
    },
    "channel_id": {
        "uk": "ID каналу «{title}»: <code>{id}</code>\nВставте його в .env як CHANNEL_ID.",
        "en": "Channel “{title}” ID: <code>{id}</code>\nPut it in .env as CHANNEL_ID.",
    },
    "admin_new_payment": {
        "uk": "💰 Нова оплата: {who} (<code>{id}</code>)\nТариф: {tariff}, {amount} ⭐",
        "en": "💰 New payment: {who} (<code>{id}</code>)\nPlan: {tariff}, {amount} ⭐",
    },
    "admin_paid_no_link": {
        "uk": "❗ Оплата пройшла, але посилання для {id} не створилося: {error}",
        "en": "❗ Payment received, but the invite link for {id} couldn't be created: {error}",
    },
    "admin_link_failed": {
        "uk": "❗ Не вдалося створити посилання для {id}: {error}",
        "en": "❗ Couldn't create an invite link for {id}: {error}",
    },
}


LANGS = ("uk", "en")


def t(lang: str, key: str, **kwargs: object) -> str:
    lang = lang if lang in LANGS else "uk"
    text = TEXTS[key][lang]
    return text.format(**kwargs) if kwargs else text
