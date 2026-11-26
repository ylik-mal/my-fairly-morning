
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.scheduler import tasks


@pytest.mark.asyncio
async def test_morning_digest_no_users():
    bot = AsyncMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_morning_time",
            new_callable=AsyncMock,
            return_value=[],
        ) as get_users,
        patch("app.scheduler.tasks.datetime") as mock_datetime,
    ):
        mock_datetime.now.return_value = datetime(2026, 11, 26, 8, 0)

        await tasks.send_morning_digest(bot)

    get_users.assert_awaited_once()
    bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_morning_digest_no_habits():
    bot = AsyncMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_morning_time",
            new_callable=AsyncMock,
            return_value=[123],
        ),
        patch(
            "app.scheduler.tasks.get_user_habits",
            new_callable=AsyncMock,
            return_value=[],
        ),
    ):
        await tasks.send_morning_digest(bot)

    bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_morning_digest_success():
    bot = AsyncMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_morning_time",
            new_callable=AsyncMock,
            return_value=[123],
        ),
        patch(
            "app.scheduler.tasks.get_user_habits",
            new_callable=AsyncMock,
            return_value=[(1, "Чтение")],
        ),
        patch(
            "app.scheduler.tasks.get_today_checkins",
            new_callable=AsyncMock,
            return_value=[],
        ),
        patch(
            "app.scheduler.tasks.get_word_topic",
            new_callable=AsyncMock,
            return_value="emotions",
        ),
        patch(
            "app.scheduler.tasks.get_word_of_the_day",
            return_value=(
                "радость",
                {"synonyms": ["счастье"], "english": ["joy"]},
            ),
        ),
        patch(
            "app.scheduler.tasks.get_random_cookie",
            return_value="Хороший день!",
        ),
        patch(
            "app.scheduler.tasks.get_habit_streak",
            new_callable=AsyncMock,
            return_value=5,
        ),
        patch(
            "app.scheduler.tasks.habits_keyboard",
            return_value="keyboard",
        ),
    ):
        await tasks.send_morning_digest(bot)

    bot.send_message.assert_awaited_once()
    kwargs = bot.send_message.await_args.kwargs

    assert kwargs["chat_id"] == 123
    assert "Доброе утро" in kwargs["text"]
    assert "РАДОСТЬ" in kwargs["text"]
    assert "5 дн." in kwargs["text"]
    assert kwargs["reply_markup"] == "keyboard"


@pytest.mark.asyncio
async def test_morning_digest_zero_streak():
    bot = AsyncMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_morning_time",
            new_callable=AsyncMock,
            return_value=[123],
        ),
        patch(
            "app.scheduler.tasks.get_user_habits",
            new_callable=AsyncMock,
            return_value=[(1, "Чтение")],
        ),
        patch(
            "app.scheduler.tasks.get_today_checkins",
            new_callable=AsyncMock,
            return_value=[],
        ),
        patch(
            "app.scheduler.tasks.get_word_topic",
            new_callable=AsyncMock,
            return_value="emotions",
        ),
        patch(
            "app.scheduler.tasks.get_word_of_the_day",
            return_value=(
                "радость",
                {"synonyms": ["счастье"], "english": ["joy"]},
            ),
        ),
        patch(
            "app.scheduler.tasks.get_random_cookie",
            return_value="Хороший день!",
        ),
        patch(
            "app.scheduler.tasks.get_habit_streak",
            new_callable=AsyncMock,
            return_value=0,
        ),
        patch(
            "app.scheduler.tasks.habits_keyboard",
            return_value="keyboard",
        ),
    ):
        await tasks.send_morning_digest(bot)

    text = bot.send_message.await_args.kwargs["text"]
    assert "Твои серии" not in text


@pytest.mark.asyncio
async def test_morning_digest_error_continues():
    bot = AsyncMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_morning_time",
            new_callable=AsyncMock,
            return_value=[123, 456],
        ),
        patch(
            "app.scheduler.tasks.get_user_habits",
            new_callable=AsyncMock,
            side_effect=[RuntimeError("Ошибка"), [(1, "Чтение")]],
        ),
        patch(
            "app.scheduler.tasks.get_today_checkins",
            new_callable=AsyncMock,
            return_value=[],
        ),
        patch(
            "app.scheduler.tasks.get_word_topic",
            new_callable=AsyncMock,
            return_value="emotions",
        ),
        patch(
            "app.scheduler.tasks.get_word_of_the_day",
            return_value=(
                "радость",
                {"synonyms": ["счастье"], "english": ["joy"]},
            ),
        ),
        patch(
            "app.scheduler.tasks.get_random_cookie",
            return_value="Хороший день!",
        ),
        patch(
            "app.scheduler.tasks.get_habit_streak",
            new_callable=AsyncMock,
            return_value=0,
        ),
        patch(
            "app.scheduler.tasks.habits_keyboard",
            return_value="keyboard",
        ),
    ):
        await tasks.send_morning_digest(bot)

    bot.send_message.assert_awaited_once()
    assert bot.send_message.await_args.kwargs["chat_id"] == 456


@pytest.mark.asyncio
async def test_evening_reflection_no_users():
    bot = AsyncMock()
    dp = MagicMock()

    with patch(
        "app.scheduler.tasks.get_users_with_evening_time",
        new_callable=AsyncMock,
        return_value=[],
    ):
        await tasks.send_evening_reflection(bot, dp)

    bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_evening_reflection_success():
    bot = AsyncMock()
    bot.id = 999

    state = AsyncMock()
    dp = MagicMock()
    dp.storage = MagicMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_evening_time",
            new_callable=AsyncMock,
            return_value=[123],
        ),
        patch(
            "app.scheduler.tasks.FSMContext",
            return_value=state,
        ) as context,
    ):
        await tasks.send_evening_reflection(bot, dp)

    context.assert_called_once()
    state.set_state.assert_awaited_once_with(
        tasks.Reflection.waiting_rating
    )
    state.update_data.assert_awaited_once_with(
        rating=None,
        success=None,
        failure=None,
    )
    bot.send_message.assert_awaited_once()

    assert bot.send_message.await_args.kwargs["chat_id"] == 123


@pytest.mark.asyncio
async def test_evening_reflection_error_continues():
    bot = AsyncMock()
    bot.id = 999

    dp = MagicMock()
    dp.storage = MagicMock()

    state = AsyncMock()

    with (
        patch(
            "app.scheduler.tasks.get_users_with_evening_time",
            new_callable=AsyncMock,
            return_value=[123, 456],
        ),
        patch(
            "app.scheduler.tasks.FSMContext",
            side_effect=[RuntimeError("Ошибка"), state],
        ),
    ):
        await tasks.send_evening_reflection(bot, dp)

    bot.send_message.assert_awaited_once()
    assert bot.send_message.await_args.kwargs["chat_id"] == 456
