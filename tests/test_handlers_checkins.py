
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def message():
    """Создаёт тестовое сообщение."""
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
    query.message.edit_reply_markup = AsyncMock()

    return query


@pytest.fixture
def services(monkeypatch):
    """Подменяет функции работы с базой данных."""
    from app.handlers import checkins

    get_habits = AsyncMock(return_value=[(5, "Чтение")])
    get_checkins = AsyncMock(return_value={})
    set_status = AsyncMock()

    monkeypatch.setattr(
        checkins, "get_user_habits", get_habits
    )
    monkeypatch.setattr(
        checkins, "get_today_checkins", get_checkins
    )
    monkeypatch.setattr(
        checkins, "set_checkin", set_status
    )

    return get_habits, get_checkins, set_status


@pytest.mark.asyncio
async def test_today_no_user(message, services):
    """Сообщение без пользователя не обрабатывается."""
    from app.handlers.checkins import send_today

    get_habits, get_checkins, _ = services
    message.from_user = None

    await send_today(message)

    get_habits.assert_not_awaited()
    get_checkins.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_today_empty(message, services):
    """При отсутствии привычек выводится подсказка."""
    from app.handlers.checkins import send_today

    get_habits, get_checkins, _ = services
    get_habits.return_value = []

    await send_today(message)

    get_habits.assert_awaited_once_with(123)
    get_checkins.assert_not_awaited()

    assert "пока нет привычек" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_today_list(message, services):
    """Команда today отображает привычки и их статусы."""
    from app.handlers.checkins import cmd_today

    get_habits, get_checkins, _ = services
    get_checkins.return_value = {5: "done"}

    await cmd_today(message)

    get_habits.assert_awaited_once_with(123)
    get_checkins.assert_awaited_once_with(123)

    keyboard = message.answer.call_args.kwargs["reply_markup"]
    button = keyboard.inline_keyboard[0][0]

    assert button.text == "✅ Чтение"
    assert button.callback_data == "checkin:5"


@pytest.mark.asyncio
async def test_habit_click_success(callback, services):
    """Выбор своей привычки открывает меню статусов."""
    from app.handlers.checkins import on_habit_click

    get_habits, _, _ = services
    callback.data = "checkin:5"

    await on_habit_click(callback)

    get_habits.assert_awaited_once_with(123)

    keyboard = (
        callback.message.edit_reply_markup
        .call_args.kwargs["reply_markup"]
    )

    assert keyboard.inline_keyboard[0][0].callback_data == "set:done:5"
    assert keyboard.inline_keyboard[1][0].callback_data == "set:skipped:5"

    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_habit_click_foreign(callback, services):
    """Нельзя выбрать чужую привычку."""
    from app.handlers.checkins import on_habit_click

    callback.data = "checkin:999"

    await on_habit_click(callback)

    callback.answer.assert_awaited_once_with("Привычка не найдена.")
    callback.message.edit_reply_markup.assert_not_awaited()


@pytest.mark.asyncio
async def test_habit_click_invalid(callback, services):
    """Некорректный идентификатор отклоняется."""
    from app.handlers.checkins import on_habit_click

    get_habits, _, _ = services
    callback.data = "checkin:abc"

    await on_habit_click(callback)

    get_habits.assert_not_awaited()
    callback.answer.assert_awaited_once_with(
        "Некорректный идентификатор привычки."
    )


@pytest.mark.asyncio
async def test_habit_click_no_data(callback, services):
    """Отсутствие данных кнопки обрабатывается безопасно."""
    from app.handlers.checkins import on_habit_click

    get_habits, _, _ = services
    callback.data = None

    await on_habit_click(callback)

    get_habits.assert_not_awaited()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_habit_click_no_message(callback, services):
    """Недоступное сообщение не редактируется."""
    from app.handlers.checkins import on_habit_click

    get_habits, _, _ = services
    callback.data = "checkin:5"
    callback.message = None

    await on_habit_click(callback)

    get_habits.assert_not_awaited()
    callback.answer.assert_awaited_once_with(
        "Сообщение недоступно."
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, expected_text",
    [
        ("done", "✅ Чтение"),
        ("skipped", "⏭ Чтение"),
    ],
)
async def test_status_set_success(
    callback, services, status, expected_text
):
    """Корректный статус сохраняется и обновляет клавиатуру."""
    from app.handlers.checkins import on_status_set

    get_habits, get_checkins, set_status = services

    callback.data = f"set:{status}:5"
    get_checkins.return_value = {5: status}

    await on_status_set(callback)

    get_habits.assert_awaited_once_with(123)

    set_status.assert_awaited_once_with(
        habit_id=5,
        user_id=123,
        status=status,
    )

    get_checkins.assert_awaited_once_with(123)

    callback.answer.assert_awaited_once_with(
        f"Отмечено: {status}"
    )

    keyboard = (
        callback.message.edit_reply_markup
        .call_args.kwargs["reply_markup"]
    )

    assert keyboard.inline_keyboard[0][0].text == expected_text


@pytest.mark.asyncio
async def test_status_set_foreign_habit(callback, services):
    """Нельзя изменить статус чужой привычки."""
    from app.handlers.checkins import on_status_set

    get_habits, get_checkins, set_status = services
    callback.data = "set:done:999"

    await on_status_set(callback)

    get_habits.assert_awaited_once_with(123)
    set_status.assert_not_awaited()
    get_checkins.assert_not_awaited()

    callback.answer.assert_awaited_once_with("Привычка не найдена.")
    callback.message.edit_reply_markup.assert_not_awaited()


@pytest.mark.asyncio
async def test_status_set_invalid_status(callback, services):
    """Неизвестный статус не сохраняется."""
    from app.handlers.checkins import on_status_set

    get_habits, _, set_status = services
    callback.data = "set:unknown:5"

    await on_status_set(callback)

    get_habits.assert_not_awaited()
    set_status.assert_not_awaited()
    callback.answer.assert_awaited_once_with("Некорректный статус.")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    ["set:done:abc", "set:done", "set:done:5:extra"],
)
async def test_status_set_invalid_data(callback, services, data):
    """Некорректные данные кнопки отклоняются."""
    from app.handlers.checkins import on_status_set

    get_habits, _, set_status = services
    callback.data = data

    await on_status_set(callback)

    get_habits.assert_not_awaited()
    set_status.assert_not_awaited()
    callback.answer.assert_awaited_once_with("Некорректные данные.")


@pytest.mark.asyncio
async def test_status_set_no_data(callback, services):
    """Отсутствие данных не приводит к записи в БД."""
    from app.handlers.checkins import on_status_set

    _, _, set_status = services
    callback.data = None

    await on_status_set(callback)

    set_status.assert_not_awaited()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_status_set_no_message(callback, services):
    """Недоступное сообщение обрабатывается безопасно."""
    from app.handlers.checkins import on_status_set

    _, _, set_status = services
    callback.data = "set:done:5"
    callback.message = None

    await on_status_set(callback)

    set_status.assert_not_awaited()
    callback.answer.assert_awaited_once_with(
        "Сообщение недоступно."
    )


@pytest.mark.asyncio
async def test_back_success(callback, services):
    """Кнопка Назад возвращает список привычек."""
    from app.handlers.checkins import on_back

    get_habits, get_checkins, _ = services
    get_checkins.return_value = {5: "done"}

    await on_back(callback)

    get_habits.assert_awaited_once_with(123)
    get_checkins.assert_awaited_once_with(123)

    keyboard = (
        callback.message.edit_reply_markup
        .call_args.kwargs["reply_markup"]
    )

    assert keyboard.inline_keyboard[0][0].text == "✅ Чтение"

    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_back_no_message(callback, services):
    """Возврат при недоступном сообщении безопасен."""
    from app.handlers.checkins import on_back

    get_habits, get_checkins, _ = services
    callback.message = None

    await on_back(callback)

    get_habits.assert_not_awaited()
    get_checkins.assert_not_awaited()
    callback.answer.assert_awaited_once_with(
        "Сообщение недоступно."
    )
