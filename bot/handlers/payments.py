import html
import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.config import Settings
from bot.db import Payment
from bot.keyboards import TariffCB, main_menu_kb
from bot.services import (
    create_invite_link,
    extend_subscription,
    get_or_create_user,
    get_subscription,
    notify_admins,
    sub_is_active,
    sub_status_text,
)
from bot.tariffs import TARIFFS
from bot.texts import t

router = Router(name="payments")
logger = logging.getLogger(__name__)

# Цифровые товары внутри бота по правилам Telegram оплачиваются только звёздами (валюта XTR).
STARS_CURRENCY = "XTR"


def make_payload(tariff_code: str, user_id: int) -> str:
    return f"sub:{tariff_code}:{user_id}"


def parse_payload(payload: str) -> tuple[str, int] | None:
    try:
        prefix, code, user_id = payload.split(":")
        if prefix != "sub" or code not in TARIFFS:
            return None
        return code, int(user_id)
    except ValueError:
        return None


@router.callback_query(TariffCB.filter())
async def on_tariff(callback: CallbackQuery, callback_data: TariffCB, session_maker: async_sessionmaker) -> None:
    tariff = TARIFFS.get(callback_data.code)
    async with session_maker() as session:
        user, _ = await get_or_create_user(session, callback.from_user)
        sub = await get_subscription(session, user.id)
        await session.commit()
    lang = user.lang

    if tariff is None:
        await callback.answer()
        return
    if sub_is_active(sub) and sub.expires_at is None:
        await callback.answer(t(lang, "already_lifetime"), show_alert=True)
        return

    await callback.bot.send_invoice(
        chat_id=user.id,
        title=tariff.title[lang],
        description=tariff.description[lang],
        payload=make_payload(tariff.code, user.id),
        currency=STARS_CURRENCY,
        prices=[LabeledPrice(label=tariff.title[lang], amount=tariff.stars)],
    )
    await callback.answer()


@router.pre_checkout_query()
async def on_pre_checkout(query: PreCheckoutQuery, session_maker: async_sessionmaker) -> None:
    """Последняя проверка перед списанием. Telegram ждёт ответ не дольше 10 секунд."""
    parsed = parse_payload(query.invoice_payload)
    tariff = TARIFFS.get(parsed[0]) if parsed else None
    valid = (
        parsed is not None
        and tariff is not None
        and parsed[1] == query.from_user.id
        and query.currency == STARS_CURRENCY
        and query.total_amount == tariff.stars
    )
    if valid:
        await query.answer(ok=True)
        return

    async with session_maker() as session:
        user, _ = await get_or_create_user(session, query.from_user)
        await session.commit()
    await query.answer(ok=False, error_message=t(user.lang, "payment_error"))


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message, session_maker: async_sessionmaker, settings: Settings, bot: Bot
) -> None:
    sp = message.successful_payment
    parsed = parse_payload(sp.invoice_payload)
    if parsed is None:
        logger.error("Unknown payload in successful payment: %s", sp.invoice_payload)
        return
    tariff = TARIFFS[parsed[0]]

    async with session_maker() as session:
        user, _ = await get_or_create_user(session, message.from_user)
        # Защита от повторной обработки одного и того же платежа.
        exists = await session.scalar(
            select(Payment.id).where(Payment.charge_id == sp.telegram_payment_charge_id)
        )
        if exists:
            return
        session.add(
            Payment(
                user_id=user.id,
                tariff=tariff.code,
                amount=sp.total_amount,
                currency=sp.currency,
                charge_id=sp.telegram_payment_charge_id,
            )
        )
        sub = await extend_subscription(session, user.id, tariff.code, tariff.days)
        await session.commit()
        status = sub_status_text(user.lang, sub)

    lang = user.lang
    try:
        link = await create_invite_link(bot, settings.channel_id, user.id)
        await message.answer(t(lang, "paid_success", status=status, link=link), reply_markup=main_menu_kb(lang))
    except TelegramBadRequest as e:
        logger.error("Invite link error after payment: %s", e)
        await message.answer(t(lang, "invite_error"), reply_markup=main_menu_kb(lang))
        await notify_admins(bot, settings.admin_ids, f"❗ Оплата прошла, но ссылка не создалась для {user.id}: {e}")

    who = f"@{user.username}" if user.username else html.escape(user.first_name or str(user.id))
    await notify_admins(
        bot,
        settings.admin_ids,
        f"💰 Новая оплата: {who} (<code>{user.id}</code>)\n"
        f"Тариф: {tariff.title['uk']}, {sp.total_amount} ⭐",
    )
