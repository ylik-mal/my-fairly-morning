import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.config import BOT_TOKEN
from app.database.db import init_db
from app.handlers import start as start_handler
from app.handlers import habits as habits_handler
from app.handlers import checkins as checkins_handler
from app.handlers import settings as settings_handler
from app.handlers import help as help_handler
from app.handlers import reflection as reflection_handler
from app.handlers import stats as stats_handler

from app.scheduler.runner import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def main() -> None:
    session = AiohttpSession(proxy="socks5://186.246.31.197:9050")
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
    dp.include_router(reflection_handler.router)
    dp.include_router(stats_handler.router)

    await init_db()

    await bot.set_my_commands([
        BotCommand(command="start", description="🏠 Перезапустить бота"),
        BotCommand(command="help", description="❓ Справка по командам"),
        BotCommand(command="add_habit", description="➕ Добавить привычку"),
        BotCommand(command="my_habits", description="📋 Мои привычки"),
        BotCommand(command="today", description="✅ Отметить привычки на сегодня"),
        BotCommand(command="set_morning", description="🌅 Время утреннего дайджеста"),
        BotCommand(command="morning", description="🌅 Текущее время дайджеста"),
        BotCommand(command="set_evening", description="🌙 Время вечерней рефлексии"),
        BotCommand(command="evening", description="🌙 Текущее время рефлексии"),
        BotCommand(command="reflect", description="📝 Начать вечернюю рефлексию"),
        BotCommand(command="my_reflections", description="📓 История рефлексий"),
        BotCommand(command="stats", description="📊 Статистика за 7 дней"),
        BotCommand(command="chart", description="📈 График за 7 дней"),          # ← новое
    ])

    start_scheduler(bot, dp)

    logging.info("Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")