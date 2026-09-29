import aiosqlite
from datetime import date as date_module

from app.config import DB_PATH


async def init_db() -> None:
    """Создаёт таблицы, если их ещё нет."""
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

        await db.commit()


async def get_or_create_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
) -> None:
    """Регистрирует пользователя, если его ещё нет."""
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
    """Добавляет привычку пользователю."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO habits (user_id, title) VALUES (?, ?)",
            (telegram_id, title),
        )
        await db.commit()


async def get_user_habits(telegram_id: int) -> list[tuple[int, str]]:
    """Возвращает список привычек пользователя в виде [(id, title), ...]."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, title FROM habits WHERE user_id = ? ORDER BY id",
            (telegram_id,),
        ) as cursor:
            return await cursor.fetchall()


async def set_checkin(habit_id: int, user_id: int, status: str) -> None:
    """Отмечает привычку как выполненную или пропущенную на сегодня."""
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
    """Возвращает dict {habit_id: status} за сегодня."""
    today = date_module.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT habit_id, status FROM checkins WHERE user_id = ? AND date = ?",
            (user_id, today),
        ) as cursor:
            rows = await cursor.fetchall()
            return {habit_id: status for habit_id, status in rows}


async def set_morning_time(user_id: int, time_str: str) -> None:
    """Сохраняет время утреннего дайджеста для пользователя."""
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
    """Возвращает время утреннего дайджеста или None."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT morning_time FROM user_settings WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_users_with_morning_time(time_str: str) -> list[int]:
    """Возвращает user_id всех, у кого утреннее время = time_str (HH:MM)."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id FROM user_settings WHERE morning_time = ?",
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
    """Сохраняет вечернюю рефлексию. Если за сегодня уже есть — обновляет."""
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
    """Возвращает последние рефлексии: [(date, rating, success, failure), ...]."""
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