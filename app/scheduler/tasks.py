import logging
from datetime import datetime

from aiogram import Bot

from app.database.db import get_today_checkins, get_user_habits, get_users_with_morning_time
from app.keyboards.checkin import habits_keyboard


logger = logging.getLogger(__name__)


async def send_morning_digest(bot: Bot) -> None:
    """Проверяет, кому сейчас нужно отправить утренний дайджест."""
    now = datetime.now().strftime("%H:%M")
    user_ids = await get_users_with_morning_time(now)

    if not user_ids:
        return

    logger.info("Утренний дайджест для %d пользователей (%s)", len(user_ids), now)

    for user_id in user_ids:
        try:
            habits = await get_user_habits(user_id)
            if not habits:
                continue

            checkins = await get_today_checkins(user_id)
            text = (
                "🌅 <b>Доброе утро!</b>\n\n"
                "📅 Привычки на сегодня:"
            )
            await bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=habits_keyboard(habits, checkins),
            )
        except Exception as e:
            logger.exception("Ошибка отправки дайджеста для %s: %s", user_id, e)