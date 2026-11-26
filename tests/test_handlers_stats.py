
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def message():
    msg = MagicMock()
    msg.from_user = SimpleNamespace(id=123)
    msg.answer = AsyncMock()
    msg.answer_photo = AsyncMock()
    return msg


@pytest.fixture
def database_mocks(monkeypatch):
    from app.handlers import stats

    get_stats = AsyncMock()
    get_streak = AsyncMock(return_value=0)

    monkeypatch.setattr(stats, "get_habits_stats", get_stats)
    monkeypatch.setattr(stats, "get_habit_streak", get_streak)

    return get_stats, get_streak


@pytest.mark.asyncio
async def test_stats_no_user(message, database_mocks):
    from app.handlers.stats import cmd_stats

    get_stats, get_streak = database_mocks
    message.from_user = None

    await cmd_stats(message)

    get_stats.assert_not_awaited()
    get_streak.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_stats_empty(message, database_mocks):
    from app.handlers.stats import cmd_stats

    get_stats, get_streak = database_mocks
    get_stats.return_value = []

    await cmd_stats(message)

    get_stats.assert_awaited_once_with(123, days=7)
    get_streak.assert_not_awaited()
    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]
    assert "/add_habit" in text


@pytest.mark.asyncio
async def test_stats_all_percentage_branches(message, database_mocks):
    from app.handlers.stats import cmd_stats

    get_stats, get_streak = database_mocks

    get_stats.return_value = [
        {"id": 1, "title": "Вода", "done": 8, "days": 10},
        {"id": 2, "title": "Чтение", "done": 5, "days": 10},
        {"id": 3, "title": "Спорт", "done": 2, "days": 10},
        {"id": 4, "title": "Английский", "done": 0, "days": 10},
    ]

    await cmd_stats(message)

    assert get_stats.await_count == 1
    assert get_streak.await_count == 4

    text = message.answer.call_args.args[0]

    assert "Вода: 8/10 (80%)" in text
    assert "Чтение: 5/10 (50%)" in text
    assert "Спорт: 2/10 (20%)" in text
    assert "Английский: 0/10 (0%)" in text

    assert "🔥" in text
    assert "✅" in text
    assert "❌" in text


@pytest.mark.asyncio
async def test_stats_positive_streak(message, database_mocks):
    from app.handlers.stats import cmd_stats

    get_stats, get_streak = database_mocks

    get_stats.return_value = [
        {"id": 1, "title": "Чтение", "done": 7, "days": 7},
    ]
    get_streak.return_value = 5

    await cmd_stats(message)

    text = message.answer.call_args.args[0]

    assert "серия: 5 дн." in text


@pytest.mark.asyncio
async def test_stats_zero_streak(message, database_mocks):
    from app.handlers.stats import cmd_stats

    get_stats, get_streak = database_mocks

    get_stats.return_value = [
        {"id": 1, "title": "Чтение", "done": 3, "days": 7},
    ]
    get_streak.return_value = 0

    await cmd_stats(message)

    text = message.answer.call_args.args[0]

    assert "Чтение: 3/7" in text
    assert "Серия:" not in text


@pytest.mark.asyncio
async def test_chart_no_user(message, monkeypatch):
    from app.handlers import stats

    generate_chart = AsyncMock()
    monkeypatch.setattr(stats, "generate_chart", generate_chart)

    message.from_user = None

    await stats.cmd_chart(message)

    generate_chart.assert_not_awaited()
    message.answer.assert_not_awaited()
    message.answer_photo.assert_not_awaited()


@pytest.mark.asyncio
async def test_chart_empty(message, monkeypatch):
    from app.handlers import stats

    generate_chart = AsyncMock(return_value=None)
    monkeypatch.setattr(stats, "generate_chart", generate_chart)

    await stats.cmd_chart(message)

    generate_chart.assert_awaited_once_with(123, days=7)
    message.answer.assert_awaited_once()
    message.answer_photo.assert_not_awaited()


@pytest.mark.asyncio
async def test_chart_success(message, monkeypatch):
    from app.handlers import stats

    generate_chart = AsyncMock(return_value=BytesIO(b"fake png data"))
    monkeypatch.setattr(stats, "generate_chart", generate_chart)

    await stats.cmd_chart(message)

    generate_chart.assert_awaited_once_with(123, days=7)

    message.answer_photo.assert_awaited_once()

    kwargs = message.answer_photo.call_args.kwargs

    assert kwargs["caption"]
    assert kwargs["photo"].filename == "chart.png"
    assert kwargs["photo"].data == b"fake png data"

    message.answer.assert_not_awaited()
