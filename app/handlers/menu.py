from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


# Структура меню: раздел → список команд
SECTIONS = {
    "habits": {
        "title": "📋 Привычки",
        "commands": [
            ("➕ Добавить привычку", "/add_habit Название"),
            ("📋 Мои привычки", "/my_habits"),
            ("✅ Отметить на сегодня", "/today"),
        ],
    },
    "reminders": {
        "title": "⏰ Напоминания",
        "commands": [
            ("🌅 Утренний дайджест", "/set_morning HH:MM"),
            ("🌅 Текущее утреннее", "/morning"),
            ("🌙 Вечерняя рефлексия", "/set_evening HH:MM"),
            ("🌙 Текущее вечернее", "/evening"),
        ],
    },
    "reflection": {
        "title": "🌙 Рефлексия",
        "commands": [
            ("📝 Начать рефлексию", "/reflect"),
            ("📓 История рефлексий", "/my_reflections"),
        ],
    },
    "analytics": {
        "title": "📊 Аналитика",
        "commands": [
            ("📊 Статистика за 7 дней", "/stats"),
            ("📈 График за 7 дней", "/chart"),
        ],
    },
    "development": {
        "title": "📚 Развитие",
        "commands": [
            ("📚 Слово дня", "/word"),
            ("🎯 Выбрать тему", "/topics"),
        ],
    },
    "help": {
        "title": "ℹ️ Помощь",
        "commands": [
            ("🏠 Перезапустить", "/start"),
            ("❓ Все команды", "/help"),
        ],
    },
}


def main_menu_keyboard():
    """Главное меню: 6 разделов в 2 колонки."""
    builder = InlineKeyboardBuilder()
    for section_key, section in SECTIONS.items():
        builder.button(
            text=section["title"],
            callback_data=f"menu:{section_key}",
        )
    builder.adjust(2)  # 2 кнопки в ряд
    return builder.as_markup()


def section_keyboard(section_key: str):
    """Подменю раздела: команды + кнопка Назад."""
    section = SECTIONS[section_key]
    builder = InlineKeyboardBuilder()

    for command_title, command_text in section["commands"]:
        builder.button(
            text=command_title,
            callback_data=f"cmd:{command_text}",
        )

    builder.button(text="⬅️ Назад", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(
        "📋 <b>Главное меню</b>\n\n"
        "Выбери раздел:",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == "menu:main")
async def back_to_main(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📋 <b>Главное меню</b>\n\n"
        "Выбери раздел:",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("menu:"))
async def open_section(callback: CallbackQuery) -> None:
    section_key = callback.data.split(":", 1)[1]

    # Если это "main" — обработается выше
    if section_key == "main":
        return

    section = SECTIONS.get(section_key)
    if not section:
        await callback.answer("Раздел не найден")
        return

    # Список команд раздела
    lines = [f"<b>{section['title']}</b>\n"]
    for command_title, command_text in section["commands"]:
        lines.append(f"• {command_title}: <code>{command_text}</code>")

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=section_keyboard(section_key),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cmd:"))
async def on_command_click(callback: CallbackQuery) -> None:
    """Показывает, какую команду нужно отправить."""
    command_text = callback.data.split(":", 1)[1]

    await callback.answer()
    await callback.message.answer(
        f"Отправь команду:\n<code>{command_text}</code>"
    )