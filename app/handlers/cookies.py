from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.utils.cookies import get_random_cookie


router = Router()


@router.message(Command("cookie"))
async def cmd_cookie(message: Message) -> None:
    cookie = get_random_cookie()

    await message.answer(
        "🥠 <b>Твоё предсказание на сегодня:</b>\n\n"
        f"<i>«{cookie}»</i>\n\n"
        "🍀 Удачного дня!"
    )