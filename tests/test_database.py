import aiosqlite
import pytest

from app.database import db


@pytest.fixture(autouse=True)
async def setup_db(isolated_db):
    """Подготавливает отдельную тестовую БД."""
    return isolated_db


@pytest.mark.asyncio
async def test_create_user():
    """Пользователь создаётся один раз, повторный вызов не дублирует."""
    await db.get_or_create_user(123, "testuser", "Test")
    await db.get_or_create_user(123, "testuser", "Test")

    async with aiosqlite.connect(db.DB_PATH) as conn, conn.execute("SELECT COUNT(*) FROM users") as cur:
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
    _date, rating, success, failure = reflections[0]
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

@pytest.mark.asyncio
async def test_delete_habit():
    """Проверяет, что привычка успешно удаляется из БД."""
    # 1. Создаём пользователя и привычку
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Временная привычка")

    # 2. Убеждаемся, что она появилась
    habits = await db.get_user_habits(123)
    assert len(habits) == 1
    habit_id = habits[0][0]

    # 3. Удаляем её
    await db.delete_habit(habit_id, 123)

    # 4. Проверяем, что список пуст
    habits_after = await db.get_user_habits(123)
    assert len(habits_after) == 0


@pytest.mark.asyncio
async def test_delete_habit_wrong_user():
    """Проверяет, что пользователь не может удалить чужую привычку."""
    # Создаём двух пользователей
    await db.get_or_create_user(123, "user1", "First")
    await db.get_or_create_user(456, "user2", "Second")

    # Первый добавляет привычку
    await db.add_habit(123, "Привычка первого")
    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    # Второй пытается её удалить
    await db.delete_habit(habit_id, 456)

    # Проверяем, что привычка на месте
    habits_after = await db.get_user_habits(123)
    assert len(habits_after) == 1


@pytest.mark.asyncio
async def test_habit_streak():
    """Проверяет правильный расчёт серии (streak) выполнения привычки."""
    from datetime import date, timedelta

    import aiosqlite

    # 1. Подготовка: создаём пользователя и привычку
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Тестовая привычка")
    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    # 2. Вручную заполняем БД отметками за 3 дня подряд (сегодня, вчера, позавчера)
    today = date.today()
    async with aiosqlite.connect(db.DB_PATH) as conn:
        for i in range(3):
            d = (today - timedelta(days=i)).isoformat()
            await conn.execute(
                "INSERT INTO checkins (habit_id, user_id, date, status) VALUES (?, ?, ?, ?)",
                (habit_id, 123, d, "done")
            )
        await conn.commit()

    # 3. Проверяем: серия должна быть 3 дня
    streak = await db.get_habit_streak(habit_id, 123)
    assert streak == 3

    # 4. Добавляем пропуск (4 дня назад — пропущено), серия всё равно 3 (она прервётся только вчера)
    async with aiosqlite.connect(db.DB_PATH) as conn:
        d4 = (today - timedelta(days=4)).isoformat()
        await conn.execute(
            "INSERT INTO checkins (habit_id, user_id, date, status) VALUES (?, ?, ?, ?)",
            (habit_id, 123, d4, "skipped")
        )
        await conn.commit()

    streak_after = await db.get_habit_streak(habit_id, 123)
    assert streak_after == 3  # ничего не изменилось, т.к. пропуск был раньше


@pytest.mark.asyncio
async def test_habit_streak_zero():
    """Если привычка не выполнялась сегодня или вчера — серия 0."""
    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Новая привычка")
    
    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    # Нет отметок вообще — серия 0
    streak = await db.get_habit_streak(habit_id, 123)
    assert streak == 0


@pytest.mark.asyncio
async def test_morning_time_default():
    """По умолчанию время утреннего уведомления не задано."""
    await db.get_or_create_user(123, "test", "Test")

    assert await db.get_morning_time(123) is None


@pytest.mark.asyncio
async def test_morning_time_saved():
    """Время утреннего уведомления сохраняется."""
    await db.get_or_create_user(123, "test", "Test")
    await db.set_morning_time(123, "08:00")

    assert await db.get_morning_time(123) == "08:00"


@pytest.mark.asyncio
async def test_morning_time_updated():
    """Новое время заменяет предыдущее."""
    await db.get_or_create_user(123, "test", "Test")
    await db.set_morning_time(123, "08:00")
    await db.set_morning_time(123, "09:30")

    assert await db.get_morning_time(123) == "09:30"


@pytest.mark.asyncio
async def test_users_with_morning_time():
    """Выбираются только пользователи с нужным временем."""
    await db.get_or_create_user(123, "first", "First")
    await db.get_or_create_user(456, "second", "Second")
    await db.get_or_create_user(789, "third", "Third")

    await db.set_morning_time(123, "08:00")
    await db.set_morning_time(456, "09:00")
    await db.set_morning_time(789, "08:00")

    users = await db.get_users_with_morning_time("08:00")

    assert sorted(users) == [123, 789]


@pytest.mark.asyncio
async def test_evening_time_default():
    """По умолчанию время вечерней рефлексии не задано."""
    await db.get_or_create_user(123, "test", "Test")

    assert await db.get_evening_time(123) is None


@pytest.mark.asyncio
async def test_evening_time_saved():
    """Время вечерней рефлексии сохраняется."""
    await db.get_or_create_user(123, "test", "Test")
    await db.set_evening_time(123, "21:00")

    assert await db.get_evening_time(123) == "21:00"


@pytest.mark.asyncio
async def test_evening_time_updated():
    """Время вечерней рефлексии можно изменить."""
    await db.get_or_create_user(123, "test", "Test")
    await db.set_evening_time(123, "21:00")
    await db.set_evening_time(123, "22:30")

    assert await db.get_evening_time(123) == "22:30"


@pytest.mark.asyncio
async def test_users_with_evening_time():
    """Выбираются пользователи с нужным временем рефлексии."""
    await db.get_or_create_user(123, "first", "First")
    await db.get_or_create_user(456, "second", "Second")
    await db.get_or_create_user(789, "third", "Third")

    await db.set_evening_time(123, "21:00")
    await db.set_evening_time(456, "22:00")
    await db.set_evening_time(789, "21:00")

    users = await db.get_users_with_evening_time("21:00")

    assert sorted(users) == [123, 789]


@pytest.mark.asyncio
async def test_morning_and_evening_independent():
    """Изменение одного уведомления не влияет на другое."""
    await db.get_or_create_user(123, "test", "Test")

    await db.set_morning_time(123, "08:00")
    await db.set_evening_time(123, "21:00")
    await db.set_morning_time(123, "09:00")

    assert await db.get_morning_time(123) == "09:00"
    assert await db.get_evening_time(123) == "21:00"


@pytest.mark.asyncio
async def test_word_topic_default():
    """Тема слова дня по умолчанию — emotions."""
    await db.get_or_create_user(123, "test", "Test")

    assert await db.get_word_topic(123) == "emotions"


@pytest.mark.asyncio
async def test_word_topic_saved():
    """Выбранная тема слова дня сохраняется."""
    await db.get_or_create_user(123, "test", "Test")
    await db.set_word_topic(123, "character")

    assert await db.get_word_topic(123) == "character"


@pytest.mark.asyncio
async def test_word_topic_updated():
    """Пользователь может изменить выбранную тему."""
    await db.get_or_create_user(123, "test", "Test")

    await db.set_word_topic(123, "character")
    await db.set_word_topic(123, "emotions")

    assert await db.get_word_topic(123) == "emotions"


@pytest.mark.asyncio
async def test_word_topic_independent():
    """Выбор темы одного пользователя не влияет на другого."""
    await db.get_or_create_user(123, "first", "First")
    await db.get_or_create_user(456, "second", "Second")

    await db.set_word_topic(123, "character")

    assert await db.get_word_topic(123) == "character"
    assert await db.get_word_topic(456) == "emotions"


@pytest.mark.asyncio
async def test_habit_streak_from_yesterday():
    """Серия сохраняется, если сегодня привычка ещё не отмечена."""
    from datetime import date, timedelta

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Чтение")

    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    today = date.today()

    async with aiosqlite.connect(db.DB_PATH) as conn:
        for i in range(1, 3):
            day = (today - timedelta(days=i)).isoformat()

            await conn.execute(
                """
                INSERT INTO checkins
                (habit_id, user_id, date, status)
                VALUES (?, ?, ?, ?)
                """,
                (habit_id, 123, day, "done"),
            )

        await conn.commit()

    streak = await db.get_habit_streak(habit_id, 123)

    assert streak == 2


@pytest.mark.asyncio
async def test_habit_streak_with_gap():
    """Пропущенный день прерывает непрерывную серию."""
    from datetime import date, timedelta

    await db.get_or_create_user(123, "test", "Test")
    await db.add_habit(123, "Чтение")

    habits = await db.get_user_habits(123)
    habit_id = habits[0][0]

    today = date.today()

    async with aiosqlite.connect(db.DB_PATH) as conn:
        for i in [0, 1, 3]:
            day = (today - timedelta(days=i)).isoformat()

            await conn.execute(
                """
                INSERT INTO checkins
                (habit_id, user_id, date, status)
                VALUES (?, ?, ?, ?)
                """,
                (habit_id, 123, day, "done"),
            )

        await conn.commit()

    streak = await db.get_habit_streak(habit_id, 123)

    assert streak == 2
