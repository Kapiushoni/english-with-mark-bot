import asyncio
import logging
from datetime import timedelta

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.config import Settings
from bot.db import Subscription, User, utcnow
from bot.keyboards import renew_kb
from bot.services import fmt_date, remove_from_channel, safe_send
from bot.texts import t

logger = logging.getLogger(__name__)


async def check_subscriptions(bot: Bot, session_maker: async_sessionmaker, settings: Settings) -> None:
    now = utcnow()
    async with session_maker() as session:
        rows = (
            await session.execute(
                select(Subscription, User)
                .join(User, User.id == Subscription.user_id)
                .where(Subscription.is_active.is_(True), Subscription.expires_at.is_not(None))
            )
        ).all()

        for sub, user in rows:
            left = sub.expires_at - now
            if left <= timedelta(0):
                await remove_from_channel(bot, settings.channel_id, user.id)
                sub.is_active = False
                await safe_send(bot, session, user.id, t(user.lang, "expired"), renew_kb(user.lang))
                logger.info("Subscription expired: user %s", user.id)
            elif left <= timedelta(days=1) and not sub.reminded_1d:
                sub.reminded_1d = True
                sub.reminded_3d = True
                await safe_send(
                    bot, session, user.id,
                    t(user.lang, "reminder_1d", date=fmt_date(sub.expires_at)), renew_kb(user.lang),
                )
            elif left <= timedelta(days=3) and not sub.reminded_3d:
                sub.reminded_3d = True
                await safe_send(
                    bot, session, user.id,
                    t(user.lang, "reminder_3d", date=fmt_date(sub.expires_at)), renew_kb(user.lang),
                )
        await session.commit()


async def subscription_watcher(bot: Bot, session_maker: async_sessionmaker, settings: Settings) -> None:
    """Фоновая задача: раз в N минут проверяет подписки."""
    while True:
        try:
            await check_subscriptions(bot, session_maker, settings)
        except Exception:
            logger.exception("Subscription check failed")
        await asyncio.sleep(settings.check_interval_minutes * 60)
