"""
Скрипт для Project CI: генерирует отчёт о состоянии проекта.
Запускается в GitHub Actions, результат сохраняется как артефакт.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import csv
from datetime import date

import aiosqlite

from app.config import DB_PATH


async def generate_report(output_path: str = "report.csv") -> None:
    """Генерирует CSV-отчёт по всем пользователям и привычкам."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            users_count = (await cur.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM habits") as cur:
            habits_count = (await cur.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM checkins") as cur:
            checkins_count = (await cur.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM reflections") as cur:
            reflections_count = (await cur.fetchone())[0]

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:  # noqa: ASYNC230
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value", "Generated at"])
        writer.writerow(["Users", users_count, date.today().isoformat()])
        writer.writerow(["Habits", habits_count, date.today().isoformat()])
        writer.writerow(["Check-ins", checkins_count, date.today().isoformat()])
        writer.writerow(["Reflections", reflections_count, date.today().isoformat()])

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        from app.database.db import init_db
        asyncio.run(init_db())
    asyncio.run(generate_report())