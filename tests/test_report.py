import os
import tempfile

import pytest

from app.config import DB_PATH
from app.database.db import init_db
from scripts.generate_report import generate_report


@pytest.mark.asyncio
async def test_generate_report():
    """Проверяет, что скрипт создаёт CSV с правильными заголовками."""
    if not os.path.exists(DB_PATH):
        await init_db()

    fd, temp_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)

    try:
        await generate_report(output_path=temp_path)
        assert os.path.exists(temp_path)
        assert os.path.getsize(temp_path) > 0

        with open(temp_path, "r", encoding="utf-8-sig") as f:  # noqa: ASYNC230
            content = f.read()
            assert "Metric,Value,Generated at" in content
            assert "Users" in content
            assert "Habits" in content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)