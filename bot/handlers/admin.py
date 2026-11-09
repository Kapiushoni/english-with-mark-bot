import asyncio
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

ADMIN_HELP = (
    "<b>Админ-панель</b>\n\n"
    "/stats — статистика\n"
    "/grant <code>user_id дни</code> — выдать доступ (например <code>/grant 123456 30</code>, "
    "<code>/grant 123456 life</code> — навсегда)\n"
    "/revoke <code>user_id</code> — закрыть доступ\n"
    "/refund <code>user_id</code> — вернуть звёзды за последнюю оплату и закрыть доступ\n"
    "/broadcast <code>текст</code> — рассылка всем пользователям бота\n\n"
    "Перешлите сюда любой пост из канала — бот покажет его ID."
)


class IsAdmin(Filter):
    async def __call__(self, message: Message, settings: Settings) -> bool:
        return message.from_user is not None and message.from_user.id in settings.admin_ids


router.message.filter(IsAdmin())


def parse_user_id(command: CommandObject) -> int | None:
    if not command.args:
        return None
    try:
        return int(command.args.split()[0])
    except ValueError:
        return None


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    await message.answer(ADMIN_HELP)


@router.message(Command("stats"))
async def cmd_stats(message: Message, session_maker: async_sessionmaker) -> None:
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
        "<b>Статистика</b>\n\n"
        f"Пользователей: {users} (заблокировали бота: {blocked})\n"
        f"Активных подписок: {active}\n"
        f"Оплат: {payments}\n"
        f"Выручка: {revenue} ⭐"
    )


@router.message(Command("grant"))
async def cmd_grant(
    message: Message, command: CommandObject, session_maker: async_sessionmaker, settings: Settings, bot: Bot
) -> None:
    args = (command.args or "").split()
    if len(args) != 2:
        await message.answer("Формат: <code>/grant user_id дни</code> или <code>/grant user_id life</code>")
        return
    try:
        user_id = int(args[0])
        days = None if args[1].lower() == "life" else int(args[1])
    except ValueError:
        await message.answer("user_id и дни должны быть числами (или life).")
        return

    async with session_maker() as session:
        user = await session.get(User, user_id)
        if not user:
            await message.answer("Этот пользователь ещё не запускал бота. Попросите его нажать /start.")
            return
        current = await get_subscription(session, user_id)
        if days is None:
            tariff_code = "lifetime"
        elif sub_is_active(current) and current.tariff in TARIFFS:
            # Активная платная подписка: продлеваем срок, тариф оставляем прежним.
            tariff_code = current.tariff
        else:
            tariff_code = "gift"
        sub = await extend_subscription(session, user_id, tariff_code, days)
        await session.commit()
        status = sub_status_text(user.lang, sub)
        lang = user.lang

        try:
            link = await create_invite_link(bot, settings.channel_id, user_id)
        except TelegramBadRequest as e:
            await message.answer(f"Доступ выдан, но ссылка не создалась: {e}")
            return
        sent = await safe_send(bot, session, user_id, t(lang, "granted", status=status, link=link))
        await session.commit()

    await message.answer(f"✅ Доступ выдан. {status}" + ("" if sent else "\n⚠️ Сообщение не доставлено."))


@router.message(Command("revoke"))
async def cmd_revoke(
    message: Message, command: CommandObject, session_maker: async_sessionmaker, settings: Settings, bot: Bot
) -> None:
    user_id = parse_user_id(command)
    if user_id is None:
        await message.answer("Формат: <code>/revoke user_id</code>")
        return
    async with session_maker() as session:
        sub = await get_subscription(session, user_id)
        if not sub:
            await message.answer("У пользователя нет подписки.")
            return
        sub.is_active = False
        await session.commit()
    await remove_from_channel(bot, settings.channel_id, user_id)
    await message.answer("✅ Доступ закрыт.")


@router.message(Command("refund"))
async def cmd_refund(
    message: Message, command: CommandObject, session_maker: async_sessionmaker, settings: Settings, bot: Bot
) -> None:
    user_id = parse_user_id(command)
    if user_id is None:
        await message.answer("Формат: <code>/refund user_id</code>")
        return
    async with session_maker() as session:
        payment = await session.scalar(
            select(Payment)
            .where(Payment.user_id == user_id, Payment.refunded.is_(False))
            .order_by(Payment.created_at.desc())
            .limit(1)
        )
        if not payment:
            await message.answer("Не найдено оплат для возврата.")
            return
        try:
            await bot.refund_star_payment(user_id=user_id, telegram_payment_charge_id=payment.charge_id)
        except TelegramBadRequest as e:
            await message.answer(f"Telegram отклонил возврат: {e}")
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
    await message.answer(f"✅ Возвращено {payment.amount} ⭐, доступ закрыт.")


@router.message(Command("broadcast"))
async def cmd_broadcast(
    message: Message, command: CommandObject, session_maker: async_sessionmaker, bot: Bot
) -> None:
    if not command.args:
        await message.answer("Формат: <code>/broadcast текст сообщения</code>")
        return
    async with session_maker() as session:
        user_ids = (await session.scalars(select(User.id).where(User.is_blocked.is_(False)))).all()
        await message.answer(f"Начинаю рассылку на {len(user_ids)} пользователей…")
        sent = 0
        for uid in user_ids:
            if await safe_send(bot, session, uid, command.args):
                sent += 1
            await asyncio.sleep(0.05)  # ~20 сообщений в секунду, в пределах лимитов Telegram
        await session.commit()
    await message.answer(f"✅ Рассылка завершена: доставлено {sent} из {len(user_ids)}.")


@router.message(F.forward_origin.type == "channel")
async def on_forward_from_channel(message: Message) -> None:
    origin = message.forward_origin
    if isinstance(origin, MessageOriginChannel):
        await message.answer(
            f"ID канала «{origin.chat.title}»: <code>{origin.chat.id}</code>\n"
            "Вставьте его в .env как CHANNEL_ID."
        )
