
"""Демонстрационный сценарий для Project CI."""

import asyncio
import csv
import json
import os
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import aiosqlite

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


async def run_demo():
    """Создаёт демонстрационные данные и формирует отчёты."""
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["DB_PATH"] = str(Path(temp_dir) / "demo.db")
        os.environ["BOT_TOKEN"] = "test_token_for_ci"

        from app.database import db
        from app.utils.charts import generate_chart
        from app.utils.csv_export import (
            generate_habits_csv,
            generate_reflections_csv,
        )

        user_id = 123456
        days = 7

        await db.init_db()
        await db.get_or_create_user(
            user_id, "demo_user", "Demo"
        )

        plan = {
            "Вода": 7,
            "Чтение": 5,
            "Спорт": 3,
            "Английский": 6,
        }

        for title in plan:
            await db.add_habit(user_id, title)

        habits = await db.get_user_habits(user_id)

        today = date.today()

        # Создаём историю выполнения за предыдущие дни.
        async with aiosqlite.connect(db.DB_PATH) as conn:
            for habit_id, title in habits:
                for offset in range(1, days):
                    day = today - timedelta(days=offset)

                    status = (
                        "done"
                        if offset < plan[title]
                        else "skipped"
                    )

                    await conn.execute(
                        """
                        INSERT INTO checkins
                            (habit_id, user_id, date, status)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            habit_id,
                            user_id,
                            day.isoformat(),
                            status,
                        ),
                    )

            # История вечерних рефлексий.
            for offset in range(1, days):
                day = today - timedelta(days=offset)

                await conn.execute(
                    """
                    INSERT INTO reflections
                        (user_id, date, rating, success, failure)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        day.isoformat(),
                        8,
                        "Demo success",
                        "Demo improvement",
                    ),
                )

            await conn.commit()

        # Сегодняшние отметки через функции приложения.
        for habit_id, _ in habits:
            await db.set_checkin(
                habit_id, user_id, "done"
            )

        await db.save_reflection(
            user_id,
            8,
            "Demo success",
            "Demo improvement",
        )

        # Рассчитываем статистику функциями бота.
        stats = await db.get_habits_stats(
            user_id, days=days
        )

        reflections = await db.get_recent_reflections(
            user_id, limit=days
        )

        total_done = sum(item["done"] for item in stats)
        total_skipped = sum(
            item["skipped"] for item in stats
        )

        total_expected = len(stats) * days

        completion = round(
            total_done / total_expected * 100, 2
        )

        ratings = [
            row[1]
            for row in reflections
            if row[1] is not None
        ]

        average_rating = sum(ratings) / len(ratings)

        report = {
            "data_type": "synthetic_demo",
            "period_days": days,
            "habits_count": len(stats),
            "completed": total_done,
            "skipped": total_skipped,
            "completion_percent": completion,
            "reflections_count": len(reflections),
            "average_rating": average_rating,
            "habits": stats,
        }

        # Проверяем точность расчётов.
        assert len(stats) == 4
        assert total_done == 21
        assert total_skipped == 7
        assert completion == 75.0
        assert len(reflections) == 7
        assert average_rating == 8.0

        for item in stats:
            assert item["done"] == plan[item["title"]]
            assert item["skipped"] == days - item["done"]

        # Используем существующие функции экспорта.
        habits_csv = await generate_habits_csv(user_id)
        reflections_csv = await generate_reflections_csv(
            user_id
        )
        chart = await generate_chart(user_id, days=days)

        assert habits_csv is not None
        assert reflections_csv is not None
        assert chart is not None

        assert chart.getvalue()[:8] == b"\x89PNG\r\n\x1a\n"

                # Проверяем содержимое CSV с привычками.
        habit_rows = list(
            csv.DictReader(
                habits_csv.getvalue()
                .decode("utf-8-sig")
                .splitlines()
            )
        )

        assert len(habit_rows) == 4

        for row in habit_rows:
            title = row["Привычка"]

            assert int(row["Выполнено (30 дн.)"]) == plan[title]
            assert int(row["Пропущено (30 дн.)"]) == days - plan[title]
            assert int(row["Всего дней"]) == 30

            expected_percent = int(plan[title] / 30 * 100)
            assert row["Процент"] == f"{expected_percent}%"

        # Проверяем содержимое CSV с рефлексиями.
        reflection_rows = list(
            csv.DictReader(
                reflections_csv.getvalue()
                .decode("utf-8-sig")
                .splitlines()
            )
        )

        assert len(reflection_rows) == 7

        for row in reflection_rows:
            assert int(row["Оценка (1-10)"]) == 8
            assert row["Что удалось"] == "Demo success"
            assert row["Что не получилось"] == "Demo improvement"

        print("CSV artifacts validated successfully.")

        output_dir = Path("demo_artifacts")
        output_dir.mkdir(exist_ok=True)

        (output_dir / "habits.csv").write_bytes(
            habits_csv.getvalue()
        )

        (output_dir / "reflections.csv").write_bytes(
            reflections_csv.getvalue()
        )

        (output_dir / "report_chart.png").write_bytes(
            chart.getvalue()
        )

        (output_dir / "report.json").write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("Demo report generated and validated successfully.")


if __name__ == "__main__":
    asyncio.run(run_demo())
