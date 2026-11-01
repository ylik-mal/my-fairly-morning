import aiosqlite
from datetime import date as date_module, timedelta

from app.config import DB_PATH


async def init_db() -> None:
    """
    Создаёт все таблицы в БД, если их ещё нет.

    Таблицы:
        - users: пользователи бота
        - habits: привычки пользователей
        - checkins: ежедневные отметки
        - user_settings: настройки времени
        - reflections: вечерние рефлексии
        - user_word_topic: выбранные темы слов
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (telegram_id) ON DELETE CASCADE
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('done', 'skipped')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (habit_id, user_id, date),
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                morning_time TEXT,
                evening_time TEXT,
                FOREIGN KEY (user_id) REFERENCES users (telegram_id) ON DELETE CASCADE
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                rating INTEGER,
                success TEXT,
                failure TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, date),
                FOREIGN KEY (user_id) REFERENCES users (telegram_id) ON DELETE CASCADE
            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS user_word_topic (
                user_id INTEGER PRIMARY KEY,
                topic TEXT NOT NULL DEFAULT 'emotions',
                FOREIGN KEY (user_id) REFERENCES users (telegram_id) ON DELETE CASCADE
            )
            """
        )

        await db.commit()


async def get_or_create_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
) -> None:
    """
    Регистрирует пользователя в БД, если его ещё нет.

    Args:
        telegram_id: Уникальный ID пользователя в Telegram.
        username: Username (без @), может быть None.
        first_name: Имя пользователя, может быть None.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (telegram_id, username, first_name)
            VALUES (?, ?, ?)
            """,
            (telegram_id, username, first_name),
        )
        await db.commit()


async def add_habit(telegram_id: int, title: str) -> None:
    """
    Добавляет новую привычку пользователю.

    Args:
        telegram_id: Telegram ID пользователя.
        title: Название привычки (например, "Выпить воды").
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO habits (user_id, title) VALUES (?, ?)",
            (telegram_id, title),
        )
        await db.commit()


async def get_user_habits(telegram_id: int) -> list[tuple[int, str]]:
    """
    Возвращает список всех привычек пользователя.

    Args:
        telegram_id: Telegram ID пользователя.

    Returns:
        Список кортежей (habit_id, title), отсортированный по ID.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, title FROM habits WHERE user_id = ? ORDER BY id",
            (telegram_id,),
        ) as cursor:
            return await cursor.fetchall()


async def set_checkin(habit_id: int, user_id: int, status: str) -> None:
    """
    Сохраняет отметку привычки за сегодня.

    Если отметка уже есть — обновляет статус.

    Args:
        habit_id: ID привычки.
        user_id: Telegram ID пользователя.
        status: "done" или "skipped".
    """
    today = date_module.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO checkins (habit_id, user_id, date, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (habit_id, user_id, date)
            DO UPDATE SET status = excluded.status
            """,
            (habit_id, user_id, today, status),
        )
        await db.commit()


async def get_today_checkins(user_id: int) -> dict[int, str]:
    """
    Возвращает все отметки пользователя за сегодня.

    Args:
        user_id: Telegram ID пользователя.

    Returns:
        Словарь {habit_id: status}, где status — "done" или "skipped".
    """
    today = date_module.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT habit_id, status FROM checkins WHERE user_id = ? AND date = ?",
            (user_id, today),
        ) as cursor:
            rows = await cursor.fetchall()
            return {habit_id: status for habit_id, status in rows}


async def set_morning_time(user_id: int, time_str: str) -> None:
    """
    Сохраняет время утреннего дайджеста.

    Args:
        user_id: Telegram ID пользователя.
        time_str: Время в формате "HH:MM" (например, "08:00").
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO user_settings (user_id, morning_time)
            VALUES (?, ?)
            ON CONFLICT (user_id)
            DO UPDATE SET morning_time = excluded.morning_time
            """,
            (user_id, time_str),
        )
        await db.commit()


async def get_morning_time(user_id: int) -> str | None:
    """
    Возвращает время утреннего дайджеста.

    Args:
        user_id: Telegram ID пользователя.

    Returns:
        Время в формате "HH:MM" или None, если не настроено.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT morning_time FROM user_settings WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_users_with_morning_time(time_str: str) -> list[int]:
    """
    Возвращает всех пользователей, у кого утренний дайджест в указанное время.

    Args:
        time_str: Время в формате "HH:MM".

    Returns:
        Список Telegram ID пользователей.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id FROM user_settings WHERE morning_time = ?",
            (time_str,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def set_evening_time(user_id: int, time_str: str) -> None:
    """
    Сохраняет время вечерней рефлексии.

    Args:
        user_id: Telegram ID пользователя.
        time_str: Время в формате "HH:MM".
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO user_settings (user_id, evening_time)
            VALUES (?, ?)
            ON CONFLICT (user_id)
            DO UPDATE SET evening_time = excluded.evening_time
            """,
            (user_id, time_str),
        )
        await db.commit()


async def get_evening_time(user_id: int) -> str | None:
    """
    Возвращает время вечерней рефлексии.

    Args:
        user_id: Telegram ID пользователя.

    Returns:
        Время в формате "HH:MM" или None.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT evening_time FROM user_settings WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_users_with_evening_time(time_str: str) -> list[int]:
    """
    Возвращает всех пользователей, у кого рефлексия в указанное время.

    Args:
        time_str: Время в формате "HH:MM".

    Returns:
        Список Telegram ID пользователей.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id FROM user_settings WHERE evening_time = ?",
            (time_str,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


async def save_reflection(
    user_id: int,
    rating: int | None,
    success: str | None,
    failure: str | None,
) -> None:
    """
    Сохраняет вечернюю рефлексию.

    Если рефлексия за сегодня уже есть — обновляет её.

    Args:
        user_id: Telegram ID пользователя.
        rating: Оценка дня от 1 до 10 (может быть None).
        success: Что удалось (может быть None).
        failure: Что не получилось (может быть None).
    """
    today = date_module.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO reflections (user_id, date, rating, success, failure)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (user_id, date)
            DO UPDATE SET
                rating = excluded.rating,
                success = excluded.success,
                failure = excluded.failure
            """,
            (user_id, today, rating, success, failure),
        )
        await db.commit()


async def get_recent_reflections(
    user_id: int,
    limit: int = 7,
) -> list[tuple[str, int | None, str | None, str | None]]:
    """
    Возвращает последние рефлексии пользователя.

    Args:
        user_id: Telegram ID пользователя.
        limit: Максимальное количество записей (по умолчанию 7).

    Returns:
        Список кортежей (date, rating, success, failure), отсортированный по дате DESC.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            """
            SELECT date, rating, success, failure
            FROM reflections
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT ?
            """,
            (user_id, limit),
        ) as cursor:
            return await cursor.fetchall()


async def get_habits_stats(user_id: int, days: int = 7) -> list[dict]:
    """
    Возвращает статистику по каждой привычке за последние N дней.

    Args:
        user_id: Telegram ID пользователя.
        days: Количество дней для анализа (по умолчанию 7).

    Returns:
        Список словарей с ключами: id, title, done, skipped, days.
    """
    today = date_module.today()
    start_date = (today - timedelta(days=days - 1)).isoformat()

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, title FROM habits WHERE user_id = ? ORDER BY id",
            (user_id,),
        ) as cursor:
            habits = await cursor.fetchall()

        result = []

        for habit_id, title in habits:
            async with db.execute(
                """
                SELECT COUNT(*) FROM checkins
                WHERE user_id = ? AND habit_id = ?
                  AND status = 'done' AND date >= ?
                """,
                (user_id, habit_id, start_date),
            ) as cursor:
                row = await cursor.fetchone()
                done_count = row[0] if row else 0

            async with db.execute(
                """
                SELECT COUNT(*) FROM checkins
                WHERE user_id = ? AND habit_id = ?
                  AND status = 'skipped' AND date >= ?
                """,
                (user_id, habit_id, start_date),
            ) as cursor:
                row = await cursor.fetchone()
                skipped_count = row[0] if row else 0

            result.append({
                "id": habit_id,
                "title": title,
                "done": done_count,
                "skipped": skipped_count,
                "days": days,
            })

        return result


async def is_new_user(telegram_id: int) -> bool:
    """
    Проверяет, новый ли пользователь (нет ли у него привычек).

    Args:
        telegram_id: Telegram ID пользователя.

    Returns:
        True, если у пользователя ещё нет привычек, иначе False.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM habits WHERE user_id = ?",
            (telegram_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return (row[0] if row else 0) == 0


async def set_word_topic(user_id: int, topic: str) -> None:
    """
    Сохраняет выбранную тему для слова дня.

    Args:
        user_id: Telegram ID пользователя.
        topic: Ключ темы (например, "emotions", "character").
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO user_word_topic (user_id, topic)
            VALUES (?, ?)
            ON CONFLICT (user_id)
            DO UPDATE SET topic = excluded.topic
            """,
            (user_id, topic),
        )
        await db.commit()


async def get_word_topic(user_id: int) -> str:
    """
    Возвращает выбранную тему для слова дня.

    Args:
        user_id: Telegram ID пользователя.

    Returns:
        Ключ темы. По умолчанию — "emotions".
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT topic FROM user_word_topic WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "emotions"


async def get_habit_streak(habit_id: int, user_id: int) -> int:
    """
    Возвращает количество дней подряд, сколько привычка выполнялась до сегодня.

    Проверяет, начиная с сегодня (или вчера, если сегодня ещё не отмечено),
    и идёт назад, пока даты идут подряд без пропусков.

    Args:
        habit_id: ID привычки.
        user_id: Telegram ID пользователя.

    Returns:
        Число дней подряд. 0, если привычка не выполнялась сегодня
        или вчера, либо если отметок вообще нет.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            """
            SELECT date FROM checkins
            WHERE habit_id = ? AND user_id = ? AND status = 'done'
            ORDER BY date DESC
            """,
            (habit_id, user_id),
        ) as cursor:
            dates = [row[0] for row in await cursor.fetchall()]

    if not dates:
        return 0

    # Проверяем, начиная с сегодня
    today = date_module.today()
    streak = 0
    check_date = today

    # Если сегодня ещё не отмечено — начинаем со вчера
    if dates[0] != today.isoformat():
        check_date = today - timedelta(days=1)

    for date_str in dates:
        if date_str == check_date.isoformat():
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return streak