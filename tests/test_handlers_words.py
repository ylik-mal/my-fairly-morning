
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import Message

from app.handlers.words import (
    TOPICS,
    cmd_topics,
    cmd_word,
    on_topic_select,
    send_word,
    topics_keyboard,
)


@pytest.mark.asyncio
async def test_topics_keyboard():
    keyboard = topics_keyboard()

    buttons = [
        button
        for row in keyboard.inline_keyboard
        for button in row
    ]

    assert len(buttons) == len(TOPICS)

    for button, (topic_key, topic_name) in zip(
        buttons, TOPICS.items()
    ):
        assert button.text == topic_name
        assert button.callback_data == f"topic:{topic_key}"


@pytest.mark.asyncio
async def test_send_word_no_user():
    message = SimpleNamespace(
        from_user=None,
        answer=AsyncMock(),
    )

    await send_word(message)

    message.answer.assert_not_awaited()


@pytest.mark.asyncio
async def test_send_word_success():
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=123),
        answer=AsyncMock(),
    )

    topic = next(iter(TOPICS))
    word_data = {
        "synonyms": ["радость", "веселье"],
        "english": ["joy", "happiness"],
    }

    with (
        patch(
            "app.handlers.words.get_word_topic",
            new_callable=AsyncMock,
            return_value=topic,
        ) as get_topic,
        patch(
            "app.handlers.words.get_word_of_the_day",
            return_value=("счастье", word_data),
        ),
    ):
        await send_word(message)

    get_topic.assert_awaited_once_with(123)

    text = message.answer.call_args.args[0]

    assert "СЧАСТЬЕ" in text
    assert TOPICS[topic] in text
    assert "радость → веселье" in text
    assert "joy / happiness" in text


@pytest.mark.asyncio
async def test_send_word_unknown_topic():
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=123),
        answer=AsyncMock(),
    )

    with (
        patch(
            "app.handlers.words.get_word_topic",
            new_callable=AsyncMock,
            return_value="unknown",
        ),
        patch(
            "app.handlers.words.get_word_of_the_day",
            return_value=(
                "слово",
                {"synonyms": ["синоним"], "english": ["word"]},
            ),
        ),
    ):
        await send_word(message)

    text = message.answer.call_args.args[0]

    assert "🎭 Эмоции и чувства" in text


@pytest.mark.asyncio
async def test_cmd_word():
    message = MagicMock()

    with patch(
        "app.handlers.words.send_word",
        new_callable=AsyncMock,
    ) as mock_send:
        await cmd_word(message)

    mock_send.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_cmd_topics():
    message = SimpleNamespace(answer=AsyncMock())

    await cmd_topics(message)

    message.answer.assert_awaited_once()

    kwargs = message.answer.call_args.kwargs

    assert "Выбери тему" in message.answer.call_args.args[0]
    assert kwargs["reply_markup"] is not None


@pytest.mark.asyncio
async def test_topic_select_no_data():
    callback = MagicMock()
    callback.data = None
    callback.answer = AsyncMock()

    await on_topic_select(callback)

    callback.answer.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_topic_select_unknown():
    callback = MagicMock()
    callback.data = "topic:unknown"
    callback.answer = AsyncMock()

    await on_topic_select(callback)

    callback.answer.assert_awaited_once_with(
        "Неизвестная тема."
    )


@pytest.mark.asyncio
async def test_topic_select_success():
    topic = next(iter(TOPICS))

    message = MagicMock(spec=Message)
    message.edit_text = AsyncMock()

    callback = MagicMock()
    callback.data = f"topic:{topic}"
    callback.from_user.id = 123
    callback.message = message
    callback.answer = AsyncMock()

    with patch(
        "app.handlers.words.set_word_topic",
        new_callable=AsyncMock,
    ) as set_topic:
        await on_topic_select(callback)

    set_topic.assert_awaited_once_with(123, topic)

    callback.answer.assert_awaited_once_with(
        f"Тема: {TOPICS[topic]}"
    )

    message.edit_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_topic_select_without_message():
    topic = next(iter(TOPICS))

    callback = MagicMock()
    callback.data = f"topic:{topic}"
    callback.from_user.id = 123
    callback.message = None
    callback.answer = AsyncMock()

    with patch(
        "app.handlers.words.set_word_topic",
        new_callable=AsyncMock,
    ) as set_topic:
        await on_topic_select(callback)

    set_topic.assert_awaited_once_with(123, topic)
    callback.answer.assert_awaited_once()
