from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from app.database.db import get_habits_stats
from app.utils.charts import generate_chart


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

    
    
@router.message(Command("chart"))
async def cmd_chart(message: Message) -> None:
    buffer = await generate_chart(message.from_user.id, days=7)

    if buffer is None:
        await message.answer(
            "Нет данных для графика.\n\n"
            "Сначала добавь привычки и отметь их через /today."
        )
        return

    photo = BufferedInputFile(
        buffer.read(),
        filename="chart.png",
    )

    await message.answer_photo(
        photo=photo,
        caption="📊 <b>Твоя статистика за 7 дней</b>",
    )