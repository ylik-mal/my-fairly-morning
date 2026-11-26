
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.types import Message

from app.handlers.menu import (
    SECTIONS,
    back_to_main,
    cmd_menu,
    main_menu_keyboard,
    on_command_click,
    open_section,
    section_keyboard,
)


@pytest.fixture
def message():
    msg = MagicMock(spec=Message)
    msg.answer = AsyncMock()
    msg.edit_text = AsyncMock()
    return msg


@pytest.fixture
def callback(message):
    cb = MagicMock()
    cb.data = "menu:habits"
    cb.message = message
    cb.answer = AsyncMock()
    cb.from_user = MagicMock(id=123)
    return cb


def test_main_menu_keyboard():
    keyboard = main_menu_keyboard()

    buttons = [
        button
        for row in keyboard.inline_keyboard
        for button in row
    ]

    assert len(buttons) == 6
    assert all(button.callback_data.startswith("menu:") for button in buttons)


@pytest.mark.parametrize("section_key", SECTIONS)
def test_section_keyboard(section_key):
    keyboard = section_keyboard(section_key)

    buttons = [
        button
        for row in keyboard.inline_keyboard
        for button in row
    ]

    assert len(buttons) == len(SECTIONS[section_key]["commands"]) + 1
    assert buttons[-1].text == "⬅️ Назад"
    assert buttons[-1].callback_data == "menu:main"


@pytest.mark.asyncio
async def test_cmd_menu(message):
    await cmd_menu(message)

    message.answer.assert_awaited_once()
    assert "Главное меню" in message.answer.call_args.args[0]


@pytest.mark.asyncio
async def test_back_to_main(callback):
    await back_to_main(callback)

    callback.message.edit_text.assert_awaited_once()
    callback.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_back_to_main_no_message(callback):
    callback.message = None

    await back_to_main(callback)

    callback.answer.assert_awaited_once_with("Сообщение недоступно.")


@pytest.mark.asyncio
async def test_open_section_no_data(callback):
    callback.data = None

    await open_section(callback)

    callback.answer.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_open_section_no_message(callback):
    callback.message = None

    await open_section(callback)

    callback.answer.assert_awaited_once_with("Сообщение недоступно.")


@pytest.mark.asyncio
async def test_open_section_main(callback):
    callback.data = "menu:main"

    await open_section(callback)

    callback.answer.assert_awaited_once()
    callback.message.edit_text.assert_not_awaited()


@pytest.mark.asyncio
async def test_open_section_unknown(callback):
    callback.data = "menu:unknown"

    await open_section(callback)

    callback.answer.assert_awaited_once_with("Раздел не найден")
    callback.message.edit_text.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("section_key", SECTIONS)
async def test_open_section_success(callback, section_key):
    callback.data = f"menu:{section_key}"

    await open_section(callback)

    callback.message.edit_text.assert_awaited_once()
    callback.answer.assert_awaited_once()

    text = callback.message.edit_text.call_args.args[0]

    assert SECTIONS[section_key]["title"] in text

    for command_title, command_text in SECTIONS[section_key]["commands"]:
        assert command_title in text
        assert command_text in text


@pytest.mark.asyncio
async def test_on_command_click_no_data(callback):
    callback.data = None

    await on_command_click(callback)

    callback.answer.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_on_command_click_no_message(callback):
    callback.message = None

    await on_command_click(callback)

    callback.answer.assert_awaited_once_with("Сообщение недоступно.")


@pytest.mark.asyncio
async def test_on_command_click_success(callback):
    callback.data = "cmd:/today"

    await on_command_click(callback)

    callback.answer.assert_awaited_once()
    callback.message.answer.assert_awaited_once_with(
        "Отправь команду:\n<code>/today</code>"
    )
