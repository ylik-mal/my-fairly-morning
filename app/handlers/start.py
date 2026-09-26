from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.db import get_or_create_user


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    # Регистрируем пользователя в БД (если ещё нет)
    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}! 🌅\n\n"
        "Я — бот <b>My Fairly Morning</b>.\n"
        "Помогу тебе выстроить утренние привычки и вечернюю рефлексию.\n\n"
        "📋 <b>Команды:</b>\n"
        "/add_habit — добавить привычку\n"
        "/my_habits — мои привычки"
    )