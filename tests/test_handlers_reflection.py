
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def message():
    """Создаёт тестовое сообщение пользователя."""
    msg = MagicMock()
    msg.from_user.id = 123
    msg.answer = AsyncMock()

    return msg


@pytest.fixture
def state():
    """Создаёт тестовый контекст FSM."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_reflect_start(message, state):
    """Рефлексия начинается с оценки дня."""
    from app.handlers.reflection import Reflection, cmd_reflect

    await cmd_reflect(message, state)

    state.set_state.assert_awaited_once_with(
        Reflection.waiting_rating
    )

    state.update_data.assert_awaited_once_with(
        rating=None,
        success=None,
        failure=None,
    )

    assert "Шаг 1/3" in message.answer.call_args.args[0]


@pytest.mark.asyncio
@pytest.mark.parametrize("rating", ["1", "5", "10", " 8 "])
async def test_rating_valid(message, state, rating):
    """Корректная оценка сохраняется."""
    from app.handlers.reflection import Reflection, process_rating

    message.text = rating

    await process_rating(message, state)

    state.update_data.assert_awaited_once_with(
        rating=int(rating)
    )

    state.set_state.assert_awaited_once_with(
        Reflection.waiting_success
    )

    assert "Шаг 2/3" in message.answer.call_args.args[0]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rating",
    [None, "", " ", "0", "11", "-1", "abc", "5.5", "²", "01"],
)
async def test_rating_invalid(message, state, rating):
    """Некорректная оценка не сохраняется."""
    from app.handlers.reflection import process_rating

    message.text = rating

    await process_rating(message, state)

    state.update_data.assert_not_awaited()
    state.set_state.assert_not_awaited()

    message.answer.assert_awaited_once_with(
        "Пожалуйста, введи число от 1 до 10."
    )


@pytest.mark.asyncio
async def test_success_valid(message, state):
    """Описание успехов сохраняется."""
    from app.handlers.reflection import Reflection, process_success

    message.text = "  Сделала домашнее задание  "

    await process_success(message, state)

    state.update_data.assert_awaited_once_with(
        success="Сделала домашнее задание"
    )

    state.set_state.assert_awaited_once_with(
        Reflection.waiting_failure
    )

    assert "Шаг 3/3" in message.answer.call_args.args[0]


@pytest.mark.asyncio
@pytest.mark.parametrize("text", [None, "", "   "])
async def test_success_empty(message, state, text):
    """Пустое описание успехов отклоняется."""
    from app.handlers.reflection import process_success

    message.text = text

    await process_success(message, state)

    state.update_data.assert_not_awaited()
    state.set_state.assert_not_awaited()

    message.answer.assert_awaited_once_with(
        "Напиши что-нибудь."
    )


@pytest.mark.asyncio
async def test_failure_valid(message, state, monkeypatch):
    """Рефлексия сохраняется, а состояние очищается."""
    from app.handlers import reflection

    save = AsyncMock()

    monkeypatch.setattr(
        reflection, "save_reflection", save
    )

    state.get_data.return_value = {
        "rating": 8,
        "success": "Сделала домашнее задание",
    }

    message.text = "  Не успела почитать  "

    await reflection.process_failure(message, state)

    save.assert_awaited_once_with(
        user_id=123,
        rating=8,
        success="Сделала домашнее задание",
        failure="Не успела почитать",
    )

    state.clear.assert_awaited_once()

    assert "Рефлексия сохранена" in message.answer.call_args.args[0]


@pytest.mark.asyncio
@pytest.mark.parametrize("text", [None, "", "   "])
async def test_failure_empty(
    message, state, monkeypatch, text
):
    """Пустое описание трудностей не сохраняется."""
    from app.handlers import reflection

    save = AsyncMock()

    monkeypatch.setattr(
        reflection, "save_reflection", save
    )

    message.text = text

    await reflection.process_failure(message, state)

    save.assert_not_awaited()
    state.get_data.assert_not_awaited()
    state.clear.assert_not_awaited()

    message.answer.assert_awaited_once_with(
        "Напиши что-нибудь."
    )


@pytest.mark.asyncio
async def test_failure_no_user(message, state, monkeypatch):
    """Без пользователя рефлексия не сохраняется."""
    from app.handlers import reflection

    save = AsyncMock()

    monkeypatch.setattr(
        reflection, "save_reflection", save
    )

    message.from_user = None
    message.text = "Не успела почитать"

    await reflection.process_failure(message, state)

    save.assert_not_awaited()
    state.clear.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_my_reflections_empty(message, monkeypatch):
    """При отсутствии рефлексий выводится подсказка."""
    from app.handlers import reflection

    get_reflections = AsyncMock(return_value=[])

    monkeypatch.setattr(
        reflection,
        "get_recent_reflections",
        get_reflections,
    )

    await reflection.cmd_my_reflections(message)

    get_reflections.assert_awaited_once_with(
        123, limit=7
    )

    assert "пока нет рефлексий" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_my_reflections_history(message, monkeypatch):
    """История содержит дату, оценку и описание дня."""
    from app.handlers import reflection

    get_reflections = AsyncMock(
        return_value=[
            (
                "2026-11-25",
                8,
                "Сделала домашнее задание",
                "Не успела почитать",
            )
        ]
    )

    monkeypatch.setattr(
        reflection,
        "get_recent_reflections",
        get_reflections,
    )

    await reflection.cmd_my_reflections(message)

    get_reflections.assert_awaited_once_with(
        123, limit=7
    )

    text = message.answer.call_args.args[0]

    assert "25.11.2026" in text
    assert "8/10" in text
    assert "Сделала домашнее задание" in text
    assert "Не успела почитать" in text


@pytest.mark.asyncio
async def test_my_reflections_missing_values(
    message, monkeypatch
):
    """Отсутствующие значения заменяются прочерками."""
    from app.handlers import reflection

    get_reflections = AsyncMock(
        return_value=[
            ("2026-11-25", None, None, None)
        ]
    )

    monkeypatch.setattr(
        reflection,
        "get_recent_reflections",
        get_reflections,
    )

    await reflection.cmd_my_reflections(message)

    text = message.answer.call_args.args[0]

    assert "Оценка: —" in text
    assert "Удалось: —" in text
    assert "Не получилось: —" in text


@pytest.mark.asyncio
async def test_my_reflections_no_user(message, monkeypatch):
    """Без пользователя история не запрашивается."""
    from app.handlers import reflection

    get_reflections = AsyncMock()

    monkeypatch.setattr(
        reflection,
        "get_recent_reflections",
        get_reflections,
    )

    message.from_user = None

    await reflection.cmd_my_reflections(message)

    get_reflections.assert_not_awaited()
    message.answer.assert_not_awaited()
