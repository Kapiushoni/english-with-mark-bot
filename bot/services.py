import logging
import time
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import User as TgUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import Subscription, User, utcnow
from bot.tariffs import TARIFFS
from bot.texts import t

logger = logging.getLogger(__name__)

INVITE_TTL_SECONDS = 24 * 60 * 60


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")


async def get_or_create_user(session: AsyncSession, tg_user: TgUser) -> tuple[User, bool]:
    user = await session.get(User, tg_user.id)
    if user:
        user.username = tg_user.username
        user.first_name = tg_user.first_name
        user.is_blocked = False
        return user, False
    lang = "uk" if (tg_user.language_code or "").startswith(("uk", "ru")) else "en"
    user = User(id=tg_user.id, username=tg_user.username, first_name=tg_user.first_name, lang=lang)
    session.add(user)
    return user, True


async def get_subscription(session: AsyncSession, user_id: int) -> Subscription | None:
    return await session.scalar(select(Subscription).where(Subscription.user_id == user_id))


def sub_is_active(sub: Subscription | None) -> bool:
    if not sub or not sub.is_active:
        return False
    return sub.expires_at is None or sub.expires_at > utcnow()


def sub_status_text(lang: str, sub: Subscription | None) -> str:
    if not sub_is_active(sub):
        return t(lang, "sub_none")
    if sub.expires_at is None:
        return t(lang, "sub_lifetime")
    tariff = TARIFFS.get(sub.tariff)
    if tariff:
        tariff_title = tariff.title[lang]
    else:  # доступ, выданный админом через /grant
        tariff_title = "Подарунковий доступ" if lang == "uk" else "Gift access"
    return t(lang, "sub_active", date=fmt_date(sub.expires_at), tariff=tariff_title)


async def extend_subscription(
    session: AsyncSession, user_id: int, tariff_code: str, days: int | None
) -> Subscription:
    """Продлевает подписку на days дней (None = навсегда). Оставшиеся дни не сгорают."""
    sub = await get_subscription(session, user_id)
    now = utcnow()

    if sub and sub_is_active(sub) and sub.expires_at is None:
        return sub  # уже навсегда, продлевать нечего

    if days is None:
        expires_at = None
    else:
        base = sub.expires_at if sub_is_active(sub) and sub.expires_at else now
        expires_at = base + timedelta(days=days)

    if sub is None:
        sub = Subscription(user_id=user_id, tariff=tariff_code, expires_at=expires_at)
        session.add(sub)
    else:
        sub.tariff = tariff_code
        sub.expires_at = expires_at
        sub.is_active = True
        sub.reminded_3d = False
        sub.reminded_1d = False
    return sub


async def create_invite_link(bot: Bot, channel_id: int, user_id: int) -> str:
    """Одноразовая ссылка: по ней может зайти только один человек, действует 24 часа."""
    link = await bot.create_chat_invite_link(
        chat_id=channel_id,
        name=f"user {user_id}"[:32],
        member_limit=1,
        expire_date=int(time.time()) + INVITE_TTL_SECONDS,
    )
    return link.invite_link


async def remove_from_channel(bot: Bot, channel_id: int, user_id: int) -> None:
    """Исключает из канала. Бан сразу снимается, чтобы человек мог вернуться после оплаты."""
    try:
        await bot.ban_chat_member(chat_id=channel_id, user_id=user_id)
        await bot.unban_chat_member(chat_id=channel_id, user_id=user_id, only_if_banned=True)
    except TelegramBadRequest as e:
        # Например, пользователь не в канале или это админ канала.
        logger.warning("Can't remove %s from channel: %s", user_id, e)


async def safe_send(
    bot: Bot,
    session: AsyncSession,
    user_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> bool:
    """Отправляет сообщение; если бот заблокирован, помечает пользователя."""
    try:
        await bot.send_message(user_id, text, reply_markup=reply_markup)
        return True
    except TelegramForbiddenError:
        user = await session.get(User, user_id)
        if user:
            user.is_blocked = True
        return False
    except TelegramBadRequest as e:
        logger.warning("Can't send message to %s: %s", user_id, e)
        return False


async def notify_admins(bot: Bot, admin_ids: set[int], text: str) -> None:
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except (TelegramBadRequest, TelegramForbiddenError):
            logger.warning("Can't notify admin %s", admin_id)
