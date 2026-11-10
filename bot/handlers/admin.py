import asyncio
import html
import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject, Filter
from aiogram.types import Message, MessageOriginChannel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.config import Settings
from bot.db import Payment, Subscription, User, utcnow
from bot.services import (
    create_invite_link,
    detect_lang,
    extend_subscription,
    get_subscription,
    remove_from_channel,
    safe_send,
    sub_is_active,
    sub_status_text,
)
from bot.tariffs import TARIFFS
from bot.texts import t

router = Router(name="admin")
logger = logging.getLogger(__name__)


class IsAdmin(Filter):
    """Lets only admins through and passes their bot language to handlers as `lang`."""

    async def __call__(
        self, message: Message, settings: Settings, session_maker: async_sessionmaker
    ) -> bool | dict[str, str]:
        if message.from_user is None or message.from_user.id not in settings.admin_ids:
            return False
        async with session_maker() as session:
            admin = await session.get(User, message.from_user.id)
        return {"lang": admin.lang if admin else detect_lang(message.from_user.language_code)}


router.message.filter(IsAdmin())


def parse_user_id(command: CommandObject) -> int | None:
    if not command.args:
        return None
    try:
        return int(command.args.split()[0])
    except ValueError:
        return None


@router.message(Command("admin"))
async def cmd_admin(message: Message, lang: str) -> None:
    await message.answer(t(lang, "admin_help"))


@router.message(Command("stats"))
async def cmd_stats(message: Message, session_maker: async_sessionmaker, lang: str) -> None:
    now = utcnow()
    async with session_maker() as session:
        users = await session.scalar(select(func.count(User.id)))
        blocked = await session.scalar(select(func.count(User.id)).where(User.is_blocked.is_(True)))
        active = await session.scalar(
            select(func.count(Subscription.id)).where(
                Subscription.is_active.is_(True),
                (Subscription.expires_at.is_(None)) | (Subscription.expires_at > now),
            )
        )
        payments = await session.scalar(select(func.count(Payment.id)).where(Payment.refunded.is_(False)))
        revenue = await session.scalar(
            select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.refunded.is_(False))
        )
    await message.answer(
        t(lang, "admin_stats", users=users, blocked=blocked, active=active, payments=payments, revenue=revenue)
    )


@router.message(Command("grant"))
async def cmd_grant(
    message: Message,
    command: CommandObject,
    session_maker: async_sessionmaker,
    settings: Settings,
    bot: Bot,
    lang: str,
) -> None:
    args = (command.args or "").split()
    if len(args) != 2:
        await message.answer(t(lang, "grant_usage"))
        return
    try:
        user_id = int(args[0])
        days = None if args[1].lower() == "life" else int(args[1])
    except ValueError:
        await message.answer(t(lang, "grant_bad_args"))
        return

    async with session_maker() as session:
        user = await session.get(User, user_id)
        if not user:
            await message.answer(t(lang, "user_not_found"))
            return
        current = await get_subscription(session, user_id)
        if days is None:
            tariff_code = "lifetime"
        elif sub_is_active(current) and current.tariff in TARIFFS:
            # Active paid subscription: extend the term, keep the same plan.
            tariff_code = current.tariff
        else:
            tariff_code = "gift"
        sub = await extend_subscription(session, user_id, tariff_code, days)
        await session.commit()
        admin_status = sub_status_text(lang, sub)

        try:
            link = await create_invite_link(bot, settings.channel_id, user_id)
        except TelegramBadRequest as e:
            await message.answer(t(lang, "grant_link_failed", error=html.escape(str(e))))
            return
        user_text = t(user.lang, "granted", status=sub_status_text(user.lang, sub), link=link)
        sent = await safe_send(bot, session, user_id, user_text)
        await session.commit()

    reply = t(lang, "grant_done", status=admin_status)
    if not sent:
        reply += "\n" + t(lang, "not_delivered")
    await message.answer(reply)


@router.message(Command("revoke"))
async def cmd_revoke(
    message: Message,
    command: CommandObject,
    session_maker: async_sessionmaker,
    settings: Settings,
    bot: Bot,
    lang: str,
) -> None:
    user_id = parse_user_id(command)
    if user_id is None:
        await message.answer(t(lang, "revoke_usage"))
        return
    async with session_maker() as session:
        sub = await get_subscription(session, user_id)
        if not sub:
            await message.answer(t(lang, "no_subscription"))
            return
        sub.is_active = False
        await session.commit()
    await remove_from_channel(bot, settings.channel_id, user_id)
    await message.answer(t(lang, "revoked"))


@router.message(Command("refund"))
async def cmd_refund(
    message: Message,
    command: CommandObject,
    session_maker: async_sessionmaker,
    settings: Settings,
    bot: Bot,
    lang: str,
) -> None:
    user_id = parse_user_id(command)
    if user_id is None:
        await message.answer(t(lang, "refund_usage"))
        return
    async with session_maker() as session:
        payment = await session.scalar(
            select(Payment)
            .where(Payment.user_id == user_id, Payment.refunded.is_(False))
            .order_by(Payment.created_at.desc())
            .limit(1)
        )
        if not payment:
            await message.answer(t(lang, "refund_not_found"))
            return
        try:
            await bot.refund_star_payment(user_id=user_id, telegram_payment_charge_id=payment.charge_id)
        except TelegramBadRequest as e:
            await message.answer(t(lang, "refund_rejected", error=html.escape(str(e))))
            return
        payment.refunded = True
        sub = await get_subscription(session, user_id)
        if sub:
            sub.is_active = False
        user = await session.get(User, user_id)
        await session.commit()
        await remove_from_channel(bot, settings.channel_id, user_id)
        if user:
            await safe_send(bot, session, user_id, t(user.lang, "refunded"))
            await session.commit()
    await message.answer(t(lang, "refund_done", amount=payment.amount))


@router.message(Command("broadcast"))
async def cmd_broadcast(
    message: Message, command: CommandObject, session_maker: async_sessionmaker, bot: Bot, lang: str
) -> None:
    if not command.args:
        await message.answer(t(lang, "broadcast_usage"))
        return
    async with session_maker() as session:
        user_ids = (await session.scalars(select(User.id).where(User.is_blocked.is_(False)))).all()
        await message.answer(t(lang, "broadcast_start", count=len(user_ids)))
        sent = 0
        for uid in user_ids:
            if await safe_send(bot, session, uid, command.args):
                sent += 1
            await asyncio.sleep(0.05)  # ~20 messages per second, within Telegram limits
        await session.commit()
    await message.answer(t(lang, "broadcast_done", sent=sent, total=len(user_ids)))


@router.message(F.forward_origin.type == "channel")
async def on_forward_from_channel(message: Message, lang: str) -> None:
    origin = message.forward_origin
    if isinstance(origin, MessageOriginChannel):
        await message.answer(t(lang, "channel_id", title=html.escape(origin.chat.title or ""), id=origin.chat.id))
