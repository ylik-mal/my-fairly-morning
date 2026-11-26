
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.db import add_habit, delete_habit, get_user_habits

router = Router()


@router.message(Command("add_habit"))
async def cmd_add_habit(message: Message) -> None:
    """Добавляет новую привычку в БД."""
    if message.text is None or message.from_user is None:
        return

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
    """Выводит список привычек с кнопками удаления."""
    if message.from_user is None:
        return

    habits = await get_user_habits(message.from_user.id)

    if not habits:
        await message.answer(
            "У тебя пока нет привычек.\n\n"
            "Добавь первую: <code>/add_habit Выпить воды</code>"
        )
        return

    lines = [f"{i}. {title}" for i, (_, title) in enumerate(habits, start=1)]
    text = "📋 <b>Твои привычки:</b>\n\n" + "\n".join(lines)

    builder = InlineKeyboardBuilder()

    for habit_id, title in habits:
        builder.button(text=f"❌ {title}", callback_data=f"del_habit:{habit_id}")

    builder.adjust(1)

    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("del_habit:"))
async def process_delete_habit(callback: CallbackQuery) -> None:
    """Удаляет привычку после нажатия на кнопку."""
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

    await delete_habit(habit_id, callback.from_user.id)

    await callback.message.edit_text("✅ Привычка успешно удалена.")
    await callback.answer()


@router.message(Command("delete_habit"))
async def cmd_delete_habit(message: Message) -> None:
    """Показывает список привычек для удаления (отдельная команда)."""
    if message.from_user is None:
        return

    habits = await get_user_habits(message.from_user.id)

    if not habits:
        await message.answer(
            "У тебя пока нет привычек, которые можно было бы удалить.\n\n"
            "Добавь первую: <code>/add_habit Выпить воды</code>"
        )
        return

    builder = InlineKeyboardBuilder()

    for habit_id, title in habits:
        builder.button(text=f"❌ {title}", callback_data=f"del_habit:{habit_id}")

    builder.adjust(1)

    await message.answer(
        "🗑 <b>Выбери привычку для удаления:</b>",
        reply_markup=builder.as_markup()
    )
