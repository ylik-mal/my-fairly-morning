
from unittest.mock import MagicMock, call, patch

from app.scheduler.runner import start_scheduler
from app.scheduler.tasks import (
    send_evening_reflection,
    send_morning_digest,
)


def test_start_scheduler():
    bot = MagicMock()
    dp = MagicMock()
    scheduler = MagicMock()

    with patch(
        "app.scheduler.runner.AsyncIOScheduler",
        return_value=scheduler,
    ) as scheduler_class:
        result = start_scheduler(bot, dp)

    scheduler_class.assert_called_once_with(
        timezone="Europe/Samara"
    )

    scheduler.add_job.assert_has_calls(
        [
            call(
                send_morning_digest,
                trigger="cron",
                minute="*",
                kwargs={"bot": bot},
                id="morning_digest",
                replace_existing=True,
            ),
            call(
                send_evening_reflection,
                trigger="cron",
                minute="*",
                kwargs={"bot": bot, "dp": dp},
                id="evening_reflection",
                replace_existing=True,
            ),
        ]
    )

    assert scheduler.add_job.call_count == 2
    scheduler.start.assert_called_once()
    assert result is scheduler
