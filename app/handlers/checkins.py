
from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.database.db import get_today_checkins, get_user_habits, set_checkin
from app.keyboards.checkin import habits_keyboard, status_keyboard

router = Router()


async def send_today(message: Message) -> None:
    """Отправляет список привычек на сегодня."""
    if message.from_user is None:
        return

    user_id = message.from_user.id
    habits = await get_user_habits(user_id)

    if not habits:
        await message.answer(
            "У тебя пока нет привычек.\n\n"
            "Добавь первую: <code>/add_habit Выпить воды</code>"
        )
        return

    checkins = await get_today_checkins(user_id)
    today = date.today().strftime("%d.%m.%Y")
    text = f"📅 <b>Привычки на {today}:</b>"
    await message.answer(text, reply_markup=habits_keyboard(habits, checkins))


@router.message(Command("today"))
async def cmd_today(message: Message) -> None:
    """Обработчик команды /today."""
    await send_today(message)


@router.callback_query(F.data.startswith("checkin:"))
async def on_habit_click(callback: CallbackQuery) -> None:
    """Обработчик нажатия на привычку."""
    if callback.data is None:
        await callback.answer()
        return

    if not isinstance(callback.message, Message):
        await callback.answer("Сообщение недоступно.")
        return

    try:
        habit_id = int(callback.data.split(":", 1)[1])
    except (ValueError, IndexError):
        await callback.answer("Некорректный идентификатор привычки.")
        return

    habits = await get_user_habits(callback.from_user.id)

    if habit_id not in [item[0] for item in habits]:
        await callback.answer("Привычка не найдена.")
        return

    await callback.message.edit_reply_markup(
        reply_markup=status_keyboard(habit_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set:"))
async def on_status_set(callback: CallbackQuery) -> None:
    """Обработчик выбора статуса."""
    if callback.data is None:
        await callback.answer()
        return

    if not isinstance(callback.message, Message):
        await callback.answer("Сообщение недоступно.")
        return

    try:
        _, status, habit_id_text = callback.data.split(":")
        habit_id = int(habit_id_text)
    except ValueError:
        await callback.answer("Некорректные данные.")
        return

    if status not in ("done", "skipped"):
        await callback.answer("Некорректный статус.")
        return

    user_id = callback.from_user.id
    habits = await get_user_habits(user_id)

    if habit_id not in [item[0] for item in habits]:
        await callback.answer("Привычка не найдена.")
        return

    await set_checkin(
        habit_id=habit_id,
        user_id=user_id,
        status=status,
    )

    await callback.answer(f"Отмечено: {status}")

    checkins = await get_today_checkins(user_id)

    await callback.message.edit_reply_markup(
        reply_markup=habits_keyboard(habits, checkins)
    )


@router.callback_query(F.data == "back:today")
async def on_back(callback: CallbackQuery) -> None:
    """Обработчик кнопки 'Назад'."""
    if not isinstance(callback.message, Message):
        await callback.answer("Сообщение недоступно.")
        return

    user_id = callback.from_user.id
    habits = await get_user_habits(user_id)
    checkins = await get_today_checkins(user_id)

    await callback.message.edit_reply_markup(
        reply_markup=habits_keyboard(habits, checkins)
    )
    await callback.answer()
