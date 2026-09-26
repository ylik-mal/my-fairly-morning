import aiosqlite

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