import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from app.config import BOT_TOKEN
from app.database.db import init_db
from app.handlers import start as start_handler
from app.handlers import habits as habits_handler
from app.handlers import checkins as checkins_handler
from app.handlers import settings as settings_handler
from app.scheduler.runner import start_scheduler
from app.handlers import help as help_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def main() -> None:
    session = AiohttpSession(proxy="socks5://185.195.71.218:18080")
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.include_router(start_handler.router)
    dp.include_router(habits_handler.router)
    dp.include_router(checkins_handler.router)
    dp.include_router(settings_handler.router)
    dp.include_router(help_handler.router)

    await init_db()

    start_scheduler(bot)

    logging.info("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")