
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def message():
    """Создаёт тестовое сообщение пользователя."""
    msg = MagicMock()
    msg.from_user.id = 123
    msg.answer = AsyncMock()

    return msg


@pytest.fixture(params=["morning", "evening"])
def settings_service(request, monkeypatch):
    """Подготавливает утренние или вечерние настройки."""
    from app.handlers import settings

    period = request.param

    if period == "morning":
        set_command = settings.cmd_set_morning
        get_command = settings.cmd_morning
    else:
        set_command = settings.cmd_set_evening
        get_command = settings.cmd_evening

    get_time = AsyncMock(return_value=None)
    set_time = AsyncMock()

    monkeypatch.setattr(
        settings, f"get_{period}_time", get_time
    )
    monkeypatch.setattr(
        settings, f"set_{period}_time", set_time
    )

    return period, set_command, get_command, get_time, set_time


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "time_str",
    ["00:00", "08:00", "12:30", "21:00", "23:59"],
)
async def test_set_time_valid(
    message, settings_service, time_str
):
    """Корректное время сохраняется."""
    period, set_command, _, _, set_time = settings_service

    message.text = f"/set_{period} {time_str}"

    await set_command(message)

    set_time.assert_awaited_once_with(123, time_str)
    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]

    assert time_str in text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "time_str",
    [
        "24:00",
        "23:60",
        "25:30",
        "8:00",
        "08:0",
        "08-00",
        "08.00",
        "abc",
        "-1:00",
        "08:00:00",
    ],
)
async def test_set_time_invalid(
    message, settings_service, time_str
):
    """Некорректное время не сохраняется."""
    period, set_command, _, _, set_time = settings_service

    message.text = f"/set_{period} {time_str}"

    await set_command(message)

    set_time.assert_not_awaited()
    message.answer.assert_awaited_once()

    assert "Неверный формат" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_set_time_with_spaces(
    message, settings_service
):
    """Лишние пробелы удаляются."""
    period, set_command, _, _, set_time = settings_service

    message.text = f"/set_{period}   08:30   "

    await set_command(message)

    set_time.assert_awaited_once_with(123, "08:30")


@pytest.mark.asyncio
async def test_set_time_without_argument(
    message, settings_service
):
    """Команда без времени выводит инструкцию."""
    period, set_command, _, get_time, set_time = settings_service

    message.text = f"/set_{period}"

    await set_command(message)

    get_time.assert_awaited_once_with(123)
    set_time.assert_not_awaited()

    text = message.answer.call_args.args[0]

    assert "HH:MM" in text
    assert "Сейчас:" not in text


@pytest.mark.asyncio
async def test_set_time_show_current(
    message, settings_service
):
    """Инструкция содержит ранее установленное время."""
    period, set_command, _, get_time, set_time = settings_service

    get_time.return_value = "09:15"
    message.text = f"/set_{period}"

    await set_command(message)

    get_time.assert_awaited_once_with(123)
    set_time.assert_not_awaited()

    text = message.answer.call_args.args[0]

    assert "Сейчас:" in text
    assert "09:15" in text


@pytest.mark.asyncio
async def test_set_time_no_text(
    message, settings_service
):
    """Сообщение без текста не обрабатывается."""
    _, set_command, _, get_time, set_time = settings_service

    message.text = None

    await set_command(message)

    get_time.assert_not_awaited()
    set_time.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_set_time_no_user(
    message, settings_service
):
    """Без пользователя настройки не сохраняются."""
    period, set_command, _, get_time, set_time = settings_service

    message.text = f"/set_{period} 08:00"
    message.from_user = None

    await set_command(message)

    get_time.assert_not_awaited()
    set_time.assert_not_awaited()
    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_time_not_configured(
    message, settings_service
):
    """Если время не настроено, выводится подсказка."""
    period, _, get_command, get_time, _ = settings_service

    get_time.return_value = None

    await get_command(message)

    get_time.assert_awaited_once_with(123)

    text = message.answer.call_args.args[0]

    assert "не настроен" in text
    assert f"/set_{period}" in text


@pytest.mark.asyncio
async def test_get_time_configured(
    message, settings_service
):
    """Отображается сохранённое время."""
    period, _, get_command, get_time, _ = settings_service

    get_time.return_value = "07:45"

    await get_command(message)

    get_time.assert_awaited_once_with(123)

    text = message.answer.call_args.args[0]

    assert "07:45" in text
    assert f"/set_{period}" in text


@pytest.mark.asyncio
async def test_get_time_no_user(
    message, settings_service
):
    """Без пользователя настройки не запрашиваются."""
    _, _, get_command, get_time, _ = settings_service

    message.from_user = None

    await get_command(message)

    get_time.assert_not_awaited()
    message.answer.assert_not_awaited()
