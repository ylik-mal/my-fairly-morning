from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🌅\n\n"
        "Я — бот <b>My Fairly Morning</b>.\n"
        "Помогу тебе выстроить утренние привычки и вечернюю рефлексию.\n\n"
        "Пока я только учусь. Скоро здесь появится список привычек и статистика."
    )