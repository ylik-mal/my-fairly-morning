import logging
from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from app.database.db import get_today_checkins, get_user_habits, get_users_with_morning_time
from app.keyboards.checkin import habits_keyboard
from app.database.db import get_users_with_evening_time
from app.handlers.reflection import Reflection


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


async def send_evening_reflection(bot: Bot, dp) -> None:
    """Проверяет, кому сейчас нужно начать вечернюю рефлексию."""
    now = datetime.now().strftime("%H:%M")
    user_ids = await get_users_with_evening_time(now)

    if not user_ids:
        return

    logger.info("Вечерняя рефлексия для %d пользователей (%s)", len(user_ids), now)

    for user_id in user_ids:
        try:
            state = FSMContext(
                storage=dp.storage,
                key=StorageKey(bot_id=bot.id, chat_id=user_id, user_id=user_id),
            )
            await state.set_state(Reflection.waiting_rating)
            await state.update_data(rating=None, success=None, failure=None)

            await bot.send_message(
                chat_id=user_id,
                text=(
                    "🌙 <b>Время вечерней рефлексии</b>\n\n"
                    "Шаг 1/3: Оцени день от 1 до 10."
                ),
            )
        except Exception as e:
            logger.exception("Ошибка вечерней рефлексии для %s: %s", user_id, e)