from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.database.db import get_today_checkins, get_user_habits, set_checkin
from app.keyboards.checkin import habits_keyboard, status_keyboard


router = Router()


async def send_today(message: Message) -> None:
    """Отправляет список привычек на сегодня."""
    habits = await get_user_habits(message.from_user.id)

    if not habits:
        await message.answer(
            "У тебя пока нет привычек.\n\n"
            "Добавь первую: <code>/add_habit Выпить воды</code>"
        )
        return

    checkins = await get_today_checkins(message.from_user.id)
    today = date.today().strftime("%d.%m.%Y")
    text = f"📅 <b>Привычки на {today}:</b>"
    await message.answer(text, reply_markup=habits_keyboard(habits, checkins))


@router.message(Command("today"))
async def cmd_today(message: Message) -> None:
    await send_today(message)


@router.callback_query(F.data.startswith("checkin:"))
async def on_habit_click(callback: CallbackQuery) -> None:
    habit_id = int(callback.data.split(":")[1])
    await callback.message.edit_reply_markup(
        reply_markup=status_keyboard(habit_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set:"))
async def on_status_set(callback: CallbackQuery) -> None:
    _, status, habit_id = callback.data.split(":")
    await set_checkin(
        habit_id=int(habit_id),
        user_id=callback.from_user.id,
        status=status,
    )
    await callback.answer(f"Отмечено: {status}")

    habits = await get_user_habits(callback.from_user.id)
    checkins = await get_today_checkins(callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=habits_keyboard(habits, checkins)
    )


@router.callback_query(F.data == "back:today")
async def on_back(callback: CallbackQuery) -> None:
    habits = await get_user_habits(callback.from_user.id)
    checkins = await get_today_checkins(callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=habits_keyboard(habits, checkins)
    )
    await callback.answer()