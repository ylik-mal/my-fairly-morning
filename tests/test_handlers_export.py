
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import Message

from app.handlers.export import (
    cmd_export,
    export_habits,
    export_keyboard,
    export_reflections,
)


def create_message():
    message = MagicMock(spec=Message)
    message.answer = AsyncMock()
    message.answer_document = AsyncMock()
    return message


def create_callback(message=None):
    return SimpleNamespace(
        message=message,
        from_user=SimpleNamespace(id=123),
        answer=AsyncMock(),
    )


def test_export_keyboard():
    keyboard = export_keyboard()

    buttons = keyboard.inline_keyboard

    assert len(buttons) == 1
    assert len(buttons[0]) == 2
    assert buttons[0][0].text == "📋 Привычки"
    assert buttons[0][0].callback_data == "export:habits"
    assert buttons[0][1].text == "📝 Рефлексии"
    assert buttons[0][1].callback_data == "export:reflections"


@pytest.mark.asyncio
async def test_cmd_export():
    message = create_message()

    await cmd_export(message)

    message.answer.assert_awaited_once()

    text = message.answer.call_args.kwargs.get(
        "text",
        message.answer.call_args.args[0]
        if message.answer.call_args.args
        else "",
    )

    assert "Что экспортировать?" in text
    assert "reply_markup" in message.answer.call_args.kwargs


@pytest.mark.asyncio
async def test_export_habits_no_message():
    callback = create_callback(message=None)

    await export_habits(callback)

    callback.answer.assert_awaited_once_with(
        "Сообщение недоступно."
    )


@pytest.mark.asyncio
async def test_export_habits_empty():
    message = create_message()
    callback = create_callback(message=message)

    with patch(
        "app.handlers.export.generate_habits_csv",
        new_callable=AsyncMock,
        return_value=None,
    ):
        await export_habits(callback)

    callback.answer.assert_awaited_once_with(
        "У тебя нет привычек для экспорта",
        show_alert=True,
    )

    message.answer_document.assert_not_awaited()


@pytest.mark.asyncio
async def test_export_habits_success():
    message = create_message()
    callback = create_callback(message=message)

    with patch(
        "app.handlers.export.generate_habits_csv",
        new_callable=AsyncMock,
        return_value=BytesIO(b"title,done\nWater,7\n"),
    ) as generate_csv:
        await export_habits(callback)

    generate_csv.assert_awaited_once_with(123)

    message.answer_document.assert_awaited_once()

    document = message.answer_document.call_args.kwargs["document"]

    assert document.filename == "habits.csv"
    assert "Твои привычки" in message.answer_document.call_args.kwargs["caption"]

    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_export_reflections_no_message():
    callback = create_callback(message=None)

    await export_reflections(callback)

    callback.answer.assert_awaited_once_with(
        "Сообщение недоступно."
    )


@pytest.mark.asyncio
async def test_export_reflections_empty():
    message = create_message()
    callback = create_callback(message=message)

    with patch(
        "app.handlers.export.generate_reflections_csv",
        new_callable=AsyncMock,
        return_value=None,
    ):
        await export_reflections(callback)

    callback.answer.assert_awaited_once_with(
        "У тебя нет рефлексий для экспорта",
        show_alert=True,
    )

    message.answer_document.assert_not_awaited()


@pytest.mark.asyncio
async def test_export_reflections_success():
    message = create_message()
    callback = create_callback(message=message)

    with patch(
        "app.handlers.export.generate_reflections_csv",
        new_callable=AsyncMock,
        return_value=BytesIO(b"date,rating\n2026-11-26,8\n"),
    ) as generate_csv:
        await export_reflections(callback)

    generate_csv.assert_awaited_once_with(123)

    message.answer_document.assert_awaited_once()

    document = message.answer_document.call_args.kwargs["document"]

    assert document.filename == "reflections.csv"
    assert "история рефлексий" in message.answer_document.call_args.kwargs["caption"]

    callback.answer.assert_awaited_once()
