import os
import tempfile

import aiosqlite
import pytest

# Тесты работают с временной БД — не трогают bot.db
TEST_DB = os.path.join(tempfile.gettempdir(), "test_bot.db")
os.environ["DB_PATH"] = TEST_DB

from app.config import DB_PATH  # noqa: E402
from app.database import db  # noqa: E402


@pytest.fixture(autouse=True)
async def setup_db():
    """Перед каждым тестом — чистая БД, после — удаляем."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    await db.init_db()

    yield

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.mark.asyncio
async def test_create_user():
    """Пользователь создаётся один раз, повторный вызов не дублирует."""
    await db.get_or_create_user(123, "testuser", "Test")
    await db.get_or_create_user(123, "testuser", "Test")

    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.execute("SELECT COUNT(*) FROM users") as cur:
            row = await cur.fetchone()
            count = row[0]

    assert count == 1


@pytest.mark.asyncio
async def test_add_habit():
    """Добавляем привычку — она появляется в списке."""
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Выпить воды")

    habits = await db.get_user_habits(123)

    assert len(habits) == 1
    assert habits[0][1] == "Выпить воды"


@pytest.mark.asyncio
async def test_multiple_habits():
    """Несколько привычек сохраняются в порядке добавления."""
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Первая")
    await db.add_habit(123, "Вторая")
    await db.add_habit(123, "Третья")

    habits = await db.get_user_habits(123)

    assert len(habits) == 3
    assert [h[1] for h in habits] == ["Первая", "Вторая", "Третья"]


@pytest.mark.asyncio
async def test_is_new_user():
    """Новый пользователь — True, после добавления привычки — False."""
    await db.get_or_create_user(123, "test", "Test")

    assert await db.is_new_user(123) is True

    await db.add_habit(123, "Привычка")

    assert await db.is_new_user(123) is False


@pytest.mark.asyncio
async def test_checkin_done():
    """Отметка 'выполнено' сохраняется и читается."""
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Привычка")

    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    await db.set_checkin(habit_id, 123, "done")

    checkins = await db.get_today_checkins(123)

    assert checkins[habit_id] == "done"


@pytest.mark.asyncio
async def test_checkin_updated():
    """Повторная отметка перезаписывает предыдущую."""
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Привычка")

    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    await db.set_checkin(habit_id, 123, "done")
    await db.set_checkin(habit_id, 123, "skipped")

    checkins = await db.get_today_checkins(123)

    assert checkins[habit_id] == "skipped"


@pytest.mark.asyncio
async def test_save_reflection():
    """Рефлексия сохраняется."""
    await db.get_or_create_user(123, "test", "Test")

    await db.save_reflection(123, rating=8, success="Всё ок", failure="Мало спал")

    reflections = await db.get_recent_reflections(123)

    assert len(reflections) == 1
    date, rating, success, failure = reflections[0]
    assert rating == 8
    assert success == "Всё ок"
    assert failure == "Мало спал"


@pytest.mark.asyncio
async def test_reflection_updated():
    """Повторная рефлексия обновляет существующую."""
    await db.get_or_create_user(123, "test", "Test")

    await db.save_reflection(123, rating=5, success="ok", failure="no")
    await db.save_reflection(123, rating=9, success="great", failure="nothing")

    reflections = await db.get_recent_reflections(123)

    assert len(reflections) == 1
    assert reflections[0][1] == 9