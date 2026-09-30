import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.db import (
    get_evening_time,
    get_morning_time,
    set_evening_time,
    set_morning_time,
)


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

@router.message(Command("set_evening"))
async def cmd_set_evening(message: Message) -> None:
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        current = await get_evening_time(message.from_user.id)
        current_line = f"\nСейчас: <b>{current}</b>" if current else ""
        await message.answer(
            "Укажи время в формате <code>HH:MM</code> (24-часовой формат)."
            f"{current_line}\n\n"
            "Например: <code>/set_evening 21:00</code>"
        )
        return

    time_str = parts[1].strip()

    if not TIME_PATTERN.match(time_str):
        await message.answer(
            "❌ Неверный формат.\n\n"
            "Используй <code>HH:MM</code>, например: <code>21:00</code>."
        )
        return

    await set_evening_time(message.from_user.id, time_str)
    await message.answer(
        f"✅ Вечерняя рефлексия установлена на <b>{time_str}</b>.\n\n"
        "Каждый день в это время я буду спрашивать, как прошёл день."
    )


@router.message(Command("evening"))
async def cmd_evening(message: Message) -> None:
    current = await get_evening_time(message.from_user.id)

    if not current:
        await message.answer(
            "Вечерняя рефлексия не настроена.\n\n"
            "Установи: <code>/set_evening 21:00</code>"
        )
        return

    await message.answer(
        f"⏰ Вечерняя рефлексия: <b>{current}</b>\n\n"
        "Изменить: <code>/set_evening HH:MM</code>"
    )