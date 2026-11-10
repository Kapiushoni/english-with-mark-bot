# English with Mark — paid channel access bot

A Telegram bot that sells access to a private Telegram channel for **Telegram Stars** and manages
subscriptions end to end: payment, single-use invite links, reminders, and automatic removal on expiry.

Built as a portfolio demo for an online English course; the same setup fits any paid community,
course, or members-only channel.

## Features

- **Bilingual UI** — Ukrainian and English, chosen by the user; admin messages follow the admin's language.
- **Three plans** — 1 month, 3 months, lifetime. Prices are configured in `.env`.
- **Native payments** — Telegram Stars invoices in the chat, with server-side validation in `pre_checkout`.
- **Secure access** — a personal single-use invite link (1 join, valid for 24 hours) after each payment.
- **Fair renewals** — remaining days are carried over when a subscription is extended.
- **Retention** — reminders 3 days and 1 day before expiry, with a one-tap renew button.
- **Automatic enforcement** — expired members are removed from the channel.
- **Admin tools** — `/stats`, `/grant`, `/revoke`, `/refund` (Stars refund), `/broadcast`, payment notifications.
- **Telegram compliance** — `/terms` and `/paysupport` commands required for Stars payments.
- **Idempotent payments** — a payment is never processed twice.

## Tech stack

- Python 3.12, [aiogram 3](https://docs.aiogram.dev/) (async)
- SQLAlchemy 2 (async) — SQLite for local runs, PostgreSQL 16 in production
- pydantic-settings for configuration
- Docker & Docker Compose (multi-arch: runs on x86 and ARM)

## Project structure

| Path | Purpose |
| --- | --- |
| `bot/texts.py` | All user and admin texts (uk / en) |
| `bot/tariffs.py` | Plans: duration, titles, descriptions |
| `bot/config.py` | Settings from environment / `.env`, including prices |
| `bot/handlers/` | User menu, payments, admin commands |
| `bot/services.py` | Subscription logic, invite links, notifications |
| `bot/scheduler.py` | Reminders and removal of expired members |

## Quick start (local)

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. Create a private channel and add the bot as an admin with permission to invite users via link
   and ban users.
3. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and set `BOT_TOKEN`.
5. Run the bot:
   ```bash
   python -m bot
   ```
6. Send `/id` to the bot, put your ID into `ADMIN_IDS`, and restart.
7. Forward any post from your channel to the bot, put the returned ID into `CHANNEL_ID`, and restart.
8. `/start` opens the user menu, `/admin` opens the admin panel.

## Deploy with Docker

```bash
cp .env.example .env                                  # fill in the values
sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$(openssl rand -hex 32)/" .env
docker compose up -d --build
docker compose logs -f bot
```

The bot and the database restart automatically; data is stored in a Docker volume.

## Testing payments

Set a plan price to `1` in `.env` (for example `PRICE_MONTH=1`), restart the bot, pay with a few Stars,
check that the invite link works, then refund with `/refund <your_id>`.

To test reminders and expiry without waiting, use `/grant <id> 1` and set `CHECK_INTERVAL_MINUTES=1`.

## Possible extensions

- Card payments via a landing page (Stripe, WayForPay, monobank) with a webhook that grants access
- Alembic migrations instead of automatic table creation
- A privacy policy for the bot
