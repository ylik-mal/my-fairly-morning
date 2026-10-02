from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.db import get_habits_stats


router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    stats = await get_habits_stats(message.from_user.id, days=7)

    if not stats:
        await message.answer(
            "У тебя нет привычек для статистики.\n\n"
            "Добавь первую: <code>/add_habit Выпить воды</code>"
        )
        return

    lines = ["📊 <b>Статистика за 7 дней:</b>\n"]
    total_done = 0

    for s in stats:
        title = s["title"]
        done = s["done"]
        days = s["days"]
        percent = int(done / days * 100)

        total_done += done

        # Эмодзи по проценту
        if percent >= 80:
            emoji = "🔥"
        elif percent >= 50:
            emoji = "✅"
        elif percent > 0:
            emoji = "⚠️"
        else:
            emoji = "❌"

        lines.append(f"{emoji} {title}: {done}/{days} ({percent}%)")

    lines.append(f"\n<b>Всего выполнений:</b> {total_done}")

    await message.answer("\n".join(lines))