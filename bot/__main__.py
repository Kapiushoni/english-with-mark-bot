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
from bot.texts import LANGS, t

logger = logging.getLogger("bot")


async def set_commands(bot: Bot) -> None:
    for lang in LANGS:
        commands = [
            BotCommand(command=cmd, description=t(lang, f"cmd_{cmd}")) for cmd in ("start", "menu", "terms", "paysupport")
        ]
        # English is also the default for clients in any other language.
        await bot.set_my_commands(commands, language_code=lang if lang != "en" else None)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = Settings()

    if settings.database_url.startswith("sqlite"):
        Path("data").mkdir(exist_ok=True)
    if not settings.admin_ids:
        logger.warning("ADMIN_IDS is not set: admin commands are disabled. Use /id to get your ID.")
    if not settings.channel_id:
        logger.warning("CHANNEL_ID is not set: forward a channel post to the bot to get its ID.")

    engine = create_async_engine(settings.database_url)
    await init_db(engine)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Everything passed to Dispatcher is available in handlers by argument name.
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
