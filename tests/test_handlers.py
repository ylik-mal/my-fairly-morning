
from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_cmd_help():
    """Команда help отправляет справку о боте."""
    from app.handlers.help import cmd_help

    message = AsyncMock()

    await cmd_help(message)

    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]

    assert "My Fairly Morning" in text
    assert "/menu" in text
    assert "/add_habit" in text
    assert "/today" in text
    assert "/reflect" in text
    assert "/stats" in text
    assert "/chart" in text
    assert "/word" in text
    assert "/cookie" in text


@pytest.mark.asyncio
async def test_cmd_cookie():
    """Команда cookie отправляет предсказание."""
    from app.handlers.cookies import cmd_cookie

    message = AsyncMock()

    await cmd_cookie(message)

    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]

    assert "Твоё предсказание на сегодня" in text
    assert "Удачного дня!" in text


@pytest.mark.asyncio
async def test_cmd_cookie_prediction(monkeypatch):
    """В ответ попадает полученное предсказание."""
    from app.handlers import cookies

    prediction = "Сегодня тебя ждёт успех!"

    monkeypatch.setattr(
        cookies,
        "get_random_cookie",
        lambda: prediction,
    )

    message = AsyncMock()

    await cookies.cmd_cookie(message)

    message.answer.assert_awaited_once()

    text = message.answer.call_args.args[0]

    assert prediction in text
