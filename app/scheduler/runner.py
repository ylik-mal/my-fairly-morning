import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduler.tasks import send_evening_reflection, send_morning_digest


logger = logging.getLogger(__name__)


def start_scheduler(bot: Bot, dp: Dispatcher) -> AsyncIOScheduler:
    """Запускает планировщик задач."""
    scheduler = AsyncIOScheduler(timezone="Europe/Samara")

    scheduler.add_job(
        send_morning_digest,
        trigger="cron",
        minute="*",
        kwargs={"bot": bot},
        id="morning_digest",
        replace_existing=True,
    )

    scheduler.add_job(
        send_evening_reflection,
        trigger="cron",
        minute="*",
        kwargs={"bot": bot, "dp": dp},
        id="evening_reflection",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Планировщик запущен")

    return scheduler