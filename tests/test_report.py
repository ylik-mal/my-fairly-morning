
import csv

import pytest


@pytest.mark.asyncio
async def test_generate_report(
    isolated_db, tmp_path, monkeypatch
):
    """Проверяет создание CSV и PNG на тестовых данных."""
    from app.database import db
    from scripts import generate_report

    monkeypatch.setattr(
        generate_report, "DB_PATH", str(isolated_db)
    )

    monkeypatch.chdir(tmp_path)

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Чтение")

    report_path = tmp_path / "report.csv"
    chart_path = tmp_path / "report_chart.png"

    await generate_report.generate_report(
        output_path=str(report_path)
    )

    assert report_path.is_file()
    assert chart_path.is_file()

    with report_path.open(
        encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        assert reader.fieldnames == [
            "Metric",
            "Value",
            "Generated at",
        ]

        metrics = {
            row["Metric"]: int(row["Value"])
            for row in reader
        }

    assert metrics == {
        "Users": 1,
        "Habits": 1,
        "Check-ins": 0,
        "Reflections": 0,
    }

    assert chart_path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
