
import os
import tempfile

import pytest

# Изолируем окружение до импорта модулей приложения.
TEST_DIR = tempfile.TemporaryDirectory()

os.environ["BOT_TOKEN"] = "test_token_for_ci"
os.environ["DB_PATH"] = os.path.join(
    TEST_DIR.name, "session.db"
)


@pytest.fixture
async def isolated_db(tmp_path, monkeypatch):
    """Создаёт отдельную базу данных для каждого теста."""
    from app.database import db

    test_db = tmp_path / "test_bot.db"

    monkeypatch.setattr(db, "DB_PATH", str(test_db))

    await db.init_db()

    return test_db


def pytest_sessionfinish(session, exitstatus):
    """Удаляет временную директорию после тестирования."""
    TEST_DIR.cleanup()
