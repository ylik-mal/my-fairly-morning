
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
def callback():
    """Создаёт тестовое нажатие на кнопку."""
    from aiogram.types import Message

    query = MagicMock()
    query.from_user.id = 123
    query.answer = AsyncMock()
    query.message = MagicMock(spec=Message)
    query.message.edit_text = AsyncMock()

    return query


@pytest.mark.asyncio
async def test_add_habit_success(message, monkeypatch):
    """Корректная привычка добавляется в базу."""
    from app.handlers import habits

    add = AsyncMock()
    monkeypatch.setattr(habits, "add_habit", add)

    message.text = "/add_habit Выпить воды"

    await habits.cmd_add_habit(message)

    add.assert_awaited_once_with(123, "Выпить воды")
    message.answer.assert_awaited_once()

    assert "Привычка добавлена" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_add_habit_without_title(message, monkeypatch):
    """Команда без названия не создаёт привычку."""
    from app.handlers import habits

    add = AsyncMock()
    monkeypatch.setattr(habits, "add_habit", add)

    message.text = "/add_habit"

    await habits.cmd_add_habit(message)

    add.assert_not_awaited()

    assert "Использование" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_add_habit_spaces(message, monkeypatch):
    """Название из пробелов не сохраняется."""
    from app.handlers import habits

    add = AsyncMock()
    monkeypatch.setattr(habits, "add_habit", add)

    message.text = "/add_habit     "

    await habits.cmd_add_habit(message)

    add.assert_not_awaited()
    message.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_habit_no_text(message, monkeypatch):
    """Сообщение без текста не обрабатывается."""
    from app.handlers import habits

    add = AsyncMock()
    monkeypatch.setattr(habits, "add_habit", add)

    message.text = None

    await habits.cmd_add_habit(message)

    add.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_add_habit_no_user(message, monkeypatch):
    """Сообщение без пользователя не обрабатывается."""
    from app.handlers import habits

    add = AsyncMock()
    monkeypatch.setattr(habits, "add_habit", add)

    message.text = "/add_habit Чтение"
    message.from_user = None

    await habits.cmd_add_habit(message)

    add.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_my_habits_empty(message, monkeypatch):
    """Пользователь получает сообщение об отсутствии привычек."""
    from app.handlers import habits

    get_habits = AsyncMock(return_value=[])
    monkeypatch.setattr(habits, "get_user_habits", get_habits)

    await habits.cmd_my_habits(message)

    get_habits.assert_awaited_once_with(123)

    assert "пока нет привычек" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_my_habits_list(message, monkeypatch):
    """Отображаются привычки и кнопки удаления."""
    from app.handlers import habits

    get_habits = AsyncMock(
        return_value=[(1, "Вода"), (2, "Чтение")]
    )
    monkeypatch.setattr(habits, "get_user_habits", get_habits)

    await habits.cmd_my_habits(message)

    get_habits.assert_awaited_once_with(123)

    text = message.answer.call_args.args[0]
    keyboard = message.answer.call_args.kwargs["reply_markup"]

    assert "1. Вода" in text
    assert "2. Чтение" in text
    assert keyboard.inline_keyboard[0][0].callback_data == "del_habit:1"
    assert keyboard.inline_keyboard[1][0].callback_data == "del_habit:2"


@pytest.mark.asyncio
async def test_my_habits_no_user(message, monkeypatch):
    """Без пользователя список не запрашивается."""
    from app.handlers import habits

    get_habits = AsyncMock()
    monkeypatch.setattr(habits, "get_user_habits", get_habits)

    message.from_user = None

    await habits.cmd_my_habits(message)

    get_habits.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_habit_menu_empty(message, monkeypatch):
    """При отсутствии привычек удалять нечего."""
    from app.handlers import habits

    get_habits = AsyncMock(return_value=[])
    monkeypatch.setattr(habits, "get_user_habits", get_habits)

    await habits.cmd_delete_habit(message)

    assert "пока нет привычек" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_delete_habit_menu(message, monkeypatch):
    """Меню содержит кнопку удаления нужной привычки."""
    from app.handlers import habits

    get_habits = AsyncMock(return_value=[(5, "Спорт")])
    monkeypatch.setattr(habits, "get_user_habits", get_habits)

    await habits.cmd_delete_habit(message)

    text = message.answer.call_args.args[0]
    keyboard = message.answer.call_args.kwargs["reply_markup"]

    assert "Выбери привычку для удаления" in text
    assert keyboard.inline_keyboard[0][0].callback_data == "del_habit:5"


@pytest.mark.asyncio
async def test_delete_habit_menu_no_user(message, monkeypatch):
    """Без пользователя меню не формируется."""
    from app.handlers import habits

    get_habits = AsyncMock()
    monkeypatch.setattr(habits, "get_user_habits", get_habits)

    message.from_user = None

    await habits.cmd_delete_habit(message)

    get_habits.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_habit_success(callback, monkeypatch):
    """Пользователь может удалить собственную привычку."""
    from app.handlers import habits

    get_habits = AsyncMock(return_value=[(5, "Спорт")])
    delete = AsyncMock()

    monkeypatch.setattr(habits, "get_user_habits", get_habits)
    monkeypatch.setattr(habits, "delete_habit", delete)

    callback.data = "del_habit:5"

    await habits.process_delete_habit(callback)

    get_habits.assert_awaited_once_with(123)
    delete.assert_awaited_once_with(5, 123)
    callback.message.edit_text.assert_awaited_once()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_foreign_habit(callback, monkeypatch):
    """Нельзя удалить привычку другого пользователя."""
    from app.handlers import habits

    get_habits = AsyncMock(return_value=[(5, "Спорт")])
    delete = AsyncMock()

    monkeypatch.setattr(habits, "get_user_habits", get_habits)
    monkeypatch.setattr(habits, "delete_habit", delete)

    callback.data = "del_habit:999"

    await habits.process_delete_habit(callback)

    get_habits.assert_awaited_once_with(123)
    delete.assert_not_awaited()
    callback.answer.assert_awaited_once_with("Привычка не найдена.")
    callback.message.edit_text.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_invalid_id(callback, monkeypatch):
    """Некорректный идентификатор не вызывает удаление."""
    from app.handlers import habits

    delete = AsyncMock()
    monkeypatch.setattr(habits, "delete_habit", delete)

    callback.data = "del_habit:abc"

    await habits.process_delete_habit(callback)

    delete.assert_not_awaited()
    callback.answer.assert_awaited_once_with(
        "Некорректный идентификатор привычки."
    )


@pytest.mark.asyncio
async def test_delete_no_callback_data(callback, monkeypatch):
    """Отсутствие данных кнопки обрабатывается безопасно."""
    from app.handlers import habits

    delete = AsyncMock()
    monkeypatch.setattr(habits, "delete_habit", delete)

    callback.data = None

    await habits.process_delete_habit(callback)

    delete.assert_not_awaited()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_no_message(callback, monkeypatch):
    """Недоступное сообщение не приводит к удалению."""
    from app.handlers import habits

    delete = AsyncMock()
    monkeypatch.setattr(habits, "delete_habit", delete)

    callback.data = "del_habit:5"
    callback.message = None

    await habits.process_delete_habit(callback)

    delete.assert_not_awaited()
    callback.answer.assert_awaited_once_with("Сообщение недоступно.")
