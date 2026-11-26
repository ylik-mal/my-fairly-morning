from io import BytesIO

import pytest


@pytest.fixture(autouse=True)
async def setup_db(isolated_db):
    """Подготавливает отдельную тестовую БД."""
    return isolated_db


@pytest.mark.asyncio
async def test_generate_chart_empty():
    """Без привычек график не создаётся."""
    from app.database import db
    from app.utils.charts import generate_chart

    await db.get_or_create_user(123, "test", "Test")

    result = await generate_chart(123)

    assert result is None


@pytest.mark.asyncio
async def test_generate_chart_png():
    """График создаётся в формате PNG."""
    from app.database import db
    from app.utils.charts import generate_chart

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Выпить воды")

    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    await db.set_checkin(habit_id, 123, "done")

    result = await generate_chart(123)

    assert isinstance(result, BytesIO)
    assert result.tell() == 0
    assert result.read(8) == b"\x89PNG\r\n\x1a\n"

    result.close()


@pytest.mark.asyncio
async def test_generate_chart_without_checkins():
    """График создаётся даже без выполненных привычек."""
    from app.database import db
    from app.utils.charts import generate_chart

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Зарядка")

    result = await generate_chart(123)

    assert isinstance(result, BytesIO)
    assert len(result.getvalue()) > 8

    result.close()


@pytest.mark.asyncio
async def test_generate_chart_long_title():
    """График поддерживает длинные названия привычек."""
    from app.database import db
    from app.utils.charts import generate_chart

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(
        123,
        "Очень длинное название ежедневной привычки",
    )

    result = await generate_chart(123)

    assert isinstance(result, BytesIO)
    assert result.read(8) == b"\x89PNG\r\n\x1a\n"

    result.close()


@pytest.mark.asyncio
async def test_generate_chart_multiple_habits():
    """График создаётся для нескольких привычек."""
    from app.database import db
    from app.utils.charts import generate_chart

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Вода")
    await db.add_habit(123, "Спорт")
    await db.add_habit(123, "Чтение")

    habits = await db.get_user_habits(123)

    await db.set_checkin(habits[0][0], 123, "done")
    await db.set_checkin(habits[1][0], 123, "skipped")

    result = await generate_chart(123, days=30)

    assert isinstance(result, BytesIO)
    assert len(result.getvalue()) > 8

    result.close()
