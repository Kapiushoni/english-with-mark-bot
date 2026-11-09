import asyncio
import logging
from contextlib import suppress
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.config import Settings
from bot.db import init_db
from bot.handlers import admin, payments, user
from bot.scheduler import subscription_watcher

logger = logging.getLogger("bot")


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Головне меню"),
            BotCommand(command="menu", description="Меню"),
            BotCommand(command="terms", description="Умови"),
            BotCommand(command="paysupport", description="Підтримка з оплат"),
        ],
        language_code="uk",
    )
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Main menu"),
            BotCommand(command="menu", description="Menu"),
            BotCommand(command="terms", description="Terms"),
            BotCommand(command="paysupport", description="Payment support"),
        ]
    )


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = Settings()

    if settings.database_url.startswith("sqlite"):
        Path("data").mkdir(exist_ok=True)
    if not settings.admin_ids:
        logger.warning("ADMIN_IDS не задан: админ-команды недоступны. Узнать свой ID — команда /id.")
    if not settings.channel_id:
        logger.warning("CHANNEL_ID не задан: перешлите боту пост из канала, чтобы узнать ID.")

    engine = create_async_engine(settings.database_url)
    await init_db(engine)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Всё, что передано в Dispatcher, доступно в хендлерах по имени аргумента.
    dp = Dispatcher(settings=settings, session_maker=session_maker)
    dp.include_routers(admin.router, payments.router, user.router)

    await set_commands(bot)
    watcher = None
    if settings.channel_id:
        watcher = asyncio.create_task(subscription_watcher(bot, session_maker, settings))

    logger.info("Bot started")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        if watcher:
            watcher.cancel()
            with suppress(asyncio.CancelledError):
                await watcher
        await engine.dispose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
