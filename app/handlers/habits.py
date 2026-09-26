from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.db import add_habit, get_user_habits


router = Router()


@router.message(Command("add_habit"))
async def cmd_add_habit(message: Message) -> None:
    # message.text = "/add_habit Выпить воды"
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.answer(
            "Использование: <code>/add_habit Название привычки</code>\n\n"
            "Например: <code>/add_habit Выпить стакан воды</code>"
        )
        return

    title = parts[1].strip()

    if not title:
        await message.answer("Название привычки не может быть пустым.")
        return

    await add_habit(message.from_user.id, title)
    await message.answer(f"✅ Привычка добавлена: <b>{title}</b>")


@router.message(Command("my_habits"))
async def cmd_my_habits(message: Message) -> None:
    habits = await get_user_habits(message.from_user.id)

    if not habits:
        await message.answer(
            "У тебя пока нет привычек.\n\n"
            "Добавь первую: <code>/add_habit Выпить воды</code>"
        )
        return

    lines = [f"{i}. {title}" for i, (_, title) in enumerate(habits, start=1)]
    text = "📋 <b>Твои привычки:</b>\n\n" + "\n".join(lines)
    await message.answer(text)