import html
import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.config import Settings
from bot.keyboards import LangCB, MenuCB, back_kb, lang_kb, main_menu_kb, my_sub_kb, tariffs_kb
from bot.services import (
    create_invite_link,
    get_or_create_user,
    get_subscription,
    notify_admins,
    sub_is_active,
    sub_status_text,
)
from bot.texts import t

router = Router(name="user")
logger = logging.getLogger(__name__)


async def show_screen(callback: CallbackQuery, text: str, kb: InlineKeyboardMarkup) -> None:
    """Редактирует текущее сообщение меню, а если нельзя — отправляет новое."""
    if isinstance(callback.message, Message):
        try:
            await callback.message.edit_text(text, reply_markup=kb)
            return
        except TelegramBadRequest:
            pass
    await callback.bot.send_message(callback.from_user.id, text, reply_markup=kb)


def welcome_text(lang: str, first_name: str | None) -> str:
    return t(lang, "welcome", name=html.escape(first_name or "👋"))


@router.message(CommandStart())
async def cmd_start(message: Message, session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        user, created = await get_or_create_user(session, message.from_user)
        await session.commit()
    if created:
        await message.answer(t(user.lang, "choose_lang"), reply_markup=lang_kb())
    else:
        await message.answer(welcome_text(user.lang, user.first_name), reply_markup=main_menu_kb(user.lang))


@router.message(Command("menu"))
async def cmd_menu(message: Message, session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        user, _ = await get_or_create_user(session, message.from_user)
        await session.commit()
    await message.answer(welcome_text(user.lang, user.first_name), reply_markup=main_menu_kb(user.lang))


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    lang = "uk" if (message.from_user.language_code or "").startswith(("uk", "ru")) else "en"
    await message.answer(t(lang, "your_id", id=message.from_user.id))


@router.message(Command("paysupport"))
async def cmd_paysupport(message: Message, session_maker: async_sessionmaker, settings: Settings) -> None:
    async with session_maker() as session:
        user, _ = await get_or_create_user(session, message.from_user)
        await session.commit()
    await message.answer(t(user.lang, "paysupport", support=settings.support_username))


@router.message(Command("terms"))
async def cmd_terms(message: Message, session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        user, _ = await get_or_create_user(session, message.from_user)
        await session.commit()
    await message.answer(t(user.lang, "terms"))


@router.callback_query(LangCB.filter())
async def on_lang(callback: CallbackQuery, callback_data: LangCB, session_maker: async_sessionmaker) -> None:
    async with session_maker() as session:
        user, _ = await get_or_create_user(session, callback.from_user)
        user.lang = callback_data.code
        await session.commit()
    await show_screen(callback, welcome_text(user.lang, user.first_name), main_menu_kb(user.lang))
    await callback.answer()


@router.callback_query(MenuCB.filter())
async def on_menu(
    callback: CallbackQuery,
    callback_data: MenuCB,
    session_maker: async_sessionmaker,
    settings: Settings,
    bot: Bot,
) -> None:
    async with session_maker() as session:
        user, _ = await get_or_create_user(session, callback.from_user)
        sub = await get_subscription(session, user.id)
        await session.commit()
    lang = user.lang
    action = callback_data.action

    if action == "tariffs":
        await show_screen(callback, t(lang, "tariffs_header"), tariffs_kb(lang))
    elif action == "renew":
        # Из уведомления: само уведомление оставляем в чате, тарифы — отдельным сообщением.
        await bot.send_message(user.id, t(lang, "tariffs_header"), reply_markup=tariffs_kb(lang))
    elif action == "my_sub":
        active = sub_is_active(sub)
        lifetime = active and sub.expires_at is None
        await show_screen(callback, sub_status_text(lang, sub), my_sub_kb(lang, active, lifetime))
    elif action == "about":
        await show_screen(callback, t(lang, "about"), back_kb(lang))
    elif action == "support":
        await show_screen(callback, t(lang, "support", support=settings.support_username), back_kb(lang))
    elif action == "lang":
        await show_screen(callback, t(lang, "choose_lang"), lang_kb())
    elif action == "link":
        if not sub_is_active(sub):
            await show_screen(callback, t(lang, "sub_none"), tariffs_kb(lang))
        else:
            try:
                link = await create_invite_link(bot, settings.channel_id, user.id)
                await bot.send_message(user.id, t(lang, "invite_link", link=link))
            except TelegramBadRequest as e:
                logger.error("Invite link error: %s", e)
                await bot.send_message(user.id, t(lang, "invite_error"))
                await notify_admins(bot, settings.admin_ids, f"❗ Не удалось создать ссылку для {user.id}: {e}")
    else:  # back
        await show_screen(callback, welcome_text(lang, user.first_name), main_menu_kb(lang))

    await callback.answer()
