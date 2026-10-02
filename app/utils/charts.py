import io

import matplotlib
matplotlib.use("Agg")  # без GUI — работает в фоне
import matplotlib.pyplot as plt

from app.database.db import get_habits_stats


async def generate_chart(user_id: int, days: int = 7) -> io.BytesIO | None:
    """Генерирует график выполнения привычек и возвращает PNG в BytesIO."""
    stats = await get_habits_stats(user_id, days=days)

    if not stats:
        return None

    titles = [s["title"] for s in stats]
    done_counts = [s["done"] for s in stats]

    # Обрезаем длинные названия
    short_titles = [t if len(t) <= 15 else t[:14] + "…" for t in titles]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(short_titles, done_counts, color="#4A90D9")

    # Числа над столбцами
    for bar, count in zip(bars, done_counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            str(count),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title(f"Выполнение привычек за {days} дней", fontsize=14, fontweight="bold")
    ax.set_ylabel("Выполнено раз", fontsize=11)
    max_val = max(done_counts) if done_counts else 1
    ax.set_ylim(0, max_val + 1 if max_val > 0 else 1)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=100)
    buffer.seek(0)
    plt.close(fig)

    return buffer