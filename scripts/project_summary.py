
"""Формирует сводку Project CI для GitHub Actions."""

import json
from pathlib import Path

report = json.loads(
    Path("demo_artifacts/report.json").read_text(
        encoding="utf-8"
    )
)

print("## 📊 My Fairly Morning — Project CI")
print()
print("Validated synthetic demo data.")
print()
print("| Metric | Result |")
print("| --- | --- |")
print(f"| Period | {report['period_days']} days |")
print(f"| Habits | {report['habits_count']} |")
print(f"| Completed | {report['completed']} |")
print(f"| Skipped | {report['skipped']} |")
print(f"| Completion | {report['completion_percent']}% |")
print(f"| Reflections | {report['reflections_count']} |")
print(f"| Average rating | {report['average_rating']}/10 |")
print()
print("### Habit statistics")
print()
print("| Habit | Completed | Skipped |")
print("| --- | --- | --- |")

for habit in report["habits"]:
    print(
        f"| {habit['title']} | "
        f"{habit['done']} | "
        f"{habit['skipped']} |"
    )

print()
print("### Available artifacts")
print()
print("| File | Description |")
print("| --- | --- |")
print("| habits.csv | Habit statistics (30 days) |")
print("| reflections.csv | Reflection history |")
print("| report.json | Weekly analytics |")
print("| report_chart.png | Weekly visualization |")
print("| demo-report.log | Execution log |")
print()
print("All artifacts are available in project-report.")
