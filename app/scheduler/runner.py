import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.scheduler.tasks import send_morning_digest


logger = logging.getLogger(__name__)


def start_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Запускает планировщик задач."""
    scheduler = AsyncIOScheduler(timezone="Europe/Samara")

    scheduler.add_job(
        send_morning_digest,
        trigger="cron",
        minute="*",  # каждую минуту
        kwargs={"bot": bot},
        id="morning_digest",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Планировщик запущен")

    return scheduler