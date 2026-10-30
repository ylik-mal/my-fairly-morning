import os
import tempfile

import pytest

# Тестовая БД
TEST_DB = os.path.join(tempfile.gettempdir(), "test_bot.db")
os.environ["DB_PATH"] = TEST_DB

from app.config import DB_PATH  # noqa: E402
from app.database import db  # noqa: E402
from app.utils.csv_export import generate_habits_csv, generate_reflections_csv  # noqa: E402


@pytest.fixture(autouse=True)
async def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    await db.init_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.mark.asyncio
async def test_generate_habits_csv():
    """CSV с привычками генерируется корректно."""
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Выпить воды")
    await db.add_habit(123, "Зарядка")

    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]
    await db.set_checkin(habit_id, 123, "done")

    buffer = await generate_habits_csv(123)
    assert buffer is not None

    content = buffer.getvalue().decode("utf-8-sig")
    lines = content.strip().split("\n")

    # Заголовок + 2 строки с привычками
    assert len(lines) >= 3
    assert "Привычка" in lines[0]
    assert "Выпить воды" in content
    assert "Зарядка" in content
    assert "✅" in content  # отметка done


@pytest.mark.asyncio
async def test_generate_habits_csv_empty():
    """Если нет привычек — возвращает None."""
    await db.get_or_create_user(123, "test", "Test")
    buffer = await generate_habits_csv(123)
    assert buffer is None


@pytest.mark.asyncio
async def test_generate_reflections_csv():
    """CSV с рефлексиями генерируется корректно."""
    await db.get_or_create_user(123, "test", "Test")
    await db.save_reflection(123, rating=8, success="Всё ок", failure="Мало спал")

    buffer = await generate_reflections_csv(123)
    assert buffer is not None

    content = buffer.getvalue().decode("utf-8-sig")
    assert "Дата" in content
    assert "8" in content
    assert "Всё ок" in content
    assert "Мало спал" in content


@pytest.mark.asyncio
async def test_generate_reflections_csv_empty():
    """Если нет рефлексий — возвращает None."""
    await db.get_or_create_user(123, "test", "Test")
    buffer = await generate_reflections_csv(123)
    assert buffer is None