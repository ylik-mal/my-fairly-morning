"""
Скрипт для Project CI: генерирует CSV-отчёт и PNG-график.
"""
import asyncio
import csv
import os
import sys
from datetime import date

import aiosqlite
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import DB_PATH


async def generate_report(output_path: str = "report.csv") -> None:
    """Генерирует CSV и график по данным БД."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            users_count = (await cur.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM habits") as cur:
            habits_count = (await cur.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM checkins") as cur:
            checkins_count = (await cur.fetchone())[0]

        async with db.execute("SELECT COUNT(*) FROM reflections") as cur:
            reflections_count = (await cur.fetchone())[0]

    # 1. Записываем CSV
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:  # noqa: ASYNC230
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value", "Generated at"])
        writer.writerow(["Users", users_count, date.today().isoformat()])
        writer.writerow(["Habits", habits_count, date.today().isoformat()])
        writer.writerow(["Check-ins", checkins_count, date.today().isoformat()])
        writer.writerow(["Reflections", reflections_count, date.today().isoformat()])

    print(f"Report generated: {output_path}")

    # 2. Генерируем график
    labels = ['Users', 'Habits', 'Check-ins', 'Reflections']
    values = [users_count, habits_count, checkins_count, reflections_count]
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=['#4A90D9', '#50C878', '#FFB347', '#FF6961'])
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')
        
    plt.title("Project Metrics")
    plt.ylabel("Count")
    plt.tight_layout()
    
    chart_path = "report_chart.png"
    plt.savefig(chart_path)
    print(f"Chart generated: {chart_path}")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        from app.database.db import init_db
        asyncio.run(init_db())
    asyncio.run(generate_report())