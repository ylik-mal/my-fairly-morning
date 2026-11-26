
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def message():
    """Создаёт тестовое сообщение от пользователя."""
    msg = MagicMock()
    msg.from_user = SimpleNamespace(
        id=123,
        username="testuser",
        first_name="Test",
    )
    msg.answer = AsyncMock()

    return msg


@pytest.fixture
def callback():
    """Создаёт тестовое нажатие на кнопку."""
    from aiogram.types import Message

    query = MagicMock()
    query.from_user = SimpleNamespace(id=123)
    query.answer = AsyncMock()
    query.message = MagicMock(spec=Message)
    query.message.answer = AsyncMock()

    return query


@pytest.fixture
def services(monkeypatch):
    """Подменяет функции обращения к базе данных."""
    from app.handlers import start

    get_or_create = AsyncMock()
    get_habits = AsyncMock(return_value=[(1, "Чтение")])
    is_new = AsyncMock(return_value=True)

    monkeypatch.setattr(
        start, "get_or_create_user", get_or_create
    )
    monkeypatch.setattr(
        start, "get_user_habits", get_habits
    )
    monkeypatch.setattr(
        start, "is_new_user", is_new
    )

    return get_or_create, get_habits, is_new


def test_welcome_keyboard():
    """Клавиатура содержит четыре кнопки с правильными callback."""
    from app.handlers.start import welcome_keyboard

    keyboard = welcome_keyboard()

    buttons = [
        button
        for row in keyboard.inline_keyboard
        for button in row
    ]

    assert len(buttons) == 4
    assert [button.callback_data for button in buttons] == [
        "menu:main",
        "welcome:add",
        "welcome:list",
        "welcome:help",
    ]


@pytest.mark.asyncio
async def test_start_no_user(message, services):
    """Команда start без пользователя ничего не делает."""
    from app.handlers.start import cmd_start

    get_or_create, _, is_new = services
    message.from_user = None

    await cmd_start(message)

    get_or_create.assert_not_awaited()
    is_new.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_start_new_user(message, services):
    """Первый запуск показывает приветствие и инструкцию."""
    from app.handlers.start import cmd_start

    get_or_create, _, is_new = services
    is_new.return_value = True

    await cmd_start(message)

    get_or_create.assert_awaited_once_with(
        telegram_id=123,
        username="testuser",
        first_name="Test",
    )
    is_new.assert_awaited_once_with(123)

    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]
    keyboard = message.answer.call_args.kwargs["reply_markup"]

    assert "My Fairly Morning" in text
    assert "/add_habit" in text
    assert "/today" in text
    assert keyboard is not None


@pytest.mark.asyncio
async def test_start_existing_user(message, services):
    """Повторный запуск показывает приветствие для вернувшегося."""
    from app.handlers.start import cmd_start

    get_or_create, _, is_new = services
    is_new.return_value = False

    await cmd_start(message)

    get_or_create.assert_awaited_once()
    is_new.assert_awaited_once_with(123)

    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]

    assert "/today" in text
    assert "/my_habits" in text


@pytest.mark.asyncio
async def test_welcome_add(callback):
    """Кнопка добавления показывает инструкцию."""
    from app.handlers.start import welcome_add

    await welcome_add(callback)

    callback.message.answer.assert_awaited_once()

    text = callback.message.answer.call_args.args[0]

    assert "/add_habit" in text
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_welcome_add_no_message(callback):
    """Кнопка добавления при недоступном сообщении."""
    from app.handlers.start import welcome_add

    callback.message = None

    await welcome_add(callback)

    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_welcome_list_empty(callback, services):
    """При отсутствии привычек выводится подсказка."""
    from app.handlers.start import welcome_list

    _, get_habits, _ = services
    get_habits.return_value = []

    await welcome_list(callback)

    get_habits.assert_awaited_once_with(123)
    callback.message.answer.assert_awaited_once()

    text = callback.message.answer.call_args.args[0]

    assert "/add_habit" in text
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_welcome_list_history(callback, services):
    """Список привычек отображается с нумерацией."""
    from app.handlers.start import welcome_list

    _, get_habits, _ = services
    get_habits.return_value = [
        (1, "Чтение"),
        (2, "Спорт"),
        (3, "Английский"),
    ]

    await welcome_list(callback)

    get_habits.assert_awaited_once_with(123)
    callback.message.answer.assert_awaited_once()

    text = callback.message.answer.call_args.args[0]

    assert "1. Чтение" in text
    assert "2. Спорт" in text
    assert "3. Английский" in text

    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_welcome_list_no_message(callback, services):
    """Список не запрашивается при недоступном сообщении."""
    from app.handlers.start import welcome_list

    _, get_habits, _ = services
    callback.message = None

    await welcome_list(callback)

    get_habits.assert_not_awaited()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_welcome_help(callback):
    """Кнопка помощи показывает список команд."""
    from app.handlers.start import welcome_help

    await welcome_help(callback)

    callback.message.answer.assert_awaited_once()

    text = callback.message.answer.call_args.args[0]

    assert "/help" in text
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_welcome_help_no_message(callback):
    """Помощь при недоступном сообщении."""
    from app.handlers.start import welcome_help

    callback.message = None

    await welcome_help(callback)

    callback.answer.assert_awaited_once()
