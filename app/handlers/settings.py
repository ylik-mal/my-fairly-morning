import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.db import get_morning_time, set_morning_time


router = Router()

TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


@router.message(Command("set_morning"))
async def cmd_set_morning(message: Message) -> None:
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        current = await get_morning_time(message.from_user.id)
        current_line = f"\nСейчас: <b>{current}</b>" if current else ""
        await message.answer(
            "Укажи время в формате <code>HH:MM</code> (24-часовой формат)."
            f"{current_line}\n\n"
            "Например: <code>/set_morning 08:00</code>"
        )
        return

    time_str = parts[1].strip()

    if not TIME_PATTERN.match(time_str):
        await message.answer(
            "❌ Неверный формат.\n\n"
            "Используй <code>HH:MM</code>, например: <code>08:00</code> или <code>21:30</code>."
        )
        return

    await set_morning_time(message.from_user.id, time_str)
    await message.answer(
        f"✅ Утренний дайджест установлен на <b>{time_str}</b>.\n\n"
        "Каждый день в это время я буду присылать список привычек."
    )


@router.message(Command("morning"))
async def cmd_morning(message: Message) -> None:
    current = await get_morning_time(message.from_user.id)

    if not current:
        await message.answer(
            "Утренний дайджест не настроен.\n\n"
            "Установи: <code>/set_morning 08:00</code>"
        )
        return

    await message.answer(
        f"⏰ Утренний дайджест: <b>{current}</b>\n\n"
        "Изменить: <code>/set_morning HH:MM</code>"
    )