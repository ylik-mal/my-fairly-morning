import csv
import io
from datetime import date

from app.database.db import (
    get_habits_stats,
    get_recent_reflections,
    get_today_checkins,
    get_user_habits,
)


async def generate_habits_csv(user_id: int) -> io.BytesIO | None:
    """Генерирует CSV с привычками и статистикой пользователя."""
    habits = await get_user_habits(user_id)
    if not habits:
        return None

    stats = await get_habits_stats(user_id, days=30)
    today = date.today().isoformat()

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # Заголовки
    writer.writerow([
        "Привычка",
        "Выполнено (30 дн.)",
        "Пропущено (30 дн.)",
        "Всего дней",
        "Процент",
        "Отметка сегодня",
    ])

    for habit_id, title in habits:
        # Находим статистику
        habit_stat = next((s for s in stats if s["id"] == habit_id), None)
        done = habit_stat["done"] if habit_stat else 0
        skipped = habit_stat["skipped"] if habit_stat else 0
        days = habit_stat["days"] if habit_stat else 30
        percent = int(done / days * 100) if days > 0 else 0

        # Сегодняшняя отметка
        checkins = await get_today_checkins(user_id)
        today_status = checkins.get(habit_id, "—")
        status_map = {"done": "✅", "skipped": "⏭", "—": "—"}
        today_text = status_map.get(today_status, "—")

        writer.writerow([
            title,
            done,
            skipped,
            days,
            f"{percent}%",
            today_text,
        ])

    # Возвращаем байты
    bytes_buffer = io.BytesIO()
    bytes_buffer.write(buffer.getvalue().encode("utf-8-sig"))  # BOM для Excel
    bytes_buffer.seek(0)

    return bytes_buffer


async def generate_reflections_csv(user_id: int) -> io.BytesIO | None:
    """Генерирует CSV с историей рефлексий."""
    reflections = await get_recent_reflections(user_id, limit=100)
    if not reflections:
        return None

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["Дата", "Оценка (1-10)", "Что удалось", "Что не получилось"])

    for date_str, rating, success, failure in reflections:
        writer.writerow([
            date_str,
            rating if rating is not None else "—",
            success or "—",
            failure or "—",
        ])

    bytes_buffer = io.BytesIO()
    bytes_buffer.write(buffer.getvalue().encode("utf-8-sig"))
    bytes_buffer.seek(0)

    return bytes_buffer