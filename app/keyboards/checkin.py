from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def habits_keyboard(
    habits: list[tuple[int, str]],
    checkins: dict[int, str],
) -> InlineKeyboardMarkup:
    """Клавиатура со списком привычек. Показывает статус за сегодня."""
    builder = InlineKeyboardBuilder()

    for habit_id, title in habits:
        status = checkins.get(habit_id)
        if status == "done":
            prefix = "✅"
        elif status == "skipped":
            prefix = "⏭"
        else:
            prefix = "⭕"

        short_title = title if len(title) <= 20 else title[:19] + "…"   # ← новая строка

        builder.button(
            text=f"{prefix} {short_title}",                             # ← изменил title на short_title
            callback_data=f"checkin:{habit_id}",
        )

    builder.adjust(1)
    return builder.as_markup()


def status_keyboard(habit_id: int) -> InlineKeyboardMarkup:
    """Кнопки выбора статуса для конкретной привычки."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Сделано", callback_data=f"set:done:{habit_id}")
    builder.button(text="⏭ Пропустить", callback_data=f"set:skipped:{habit_id}")
    builder.button(text="⬅️ Назад", callback_data="back:today")
    builder.adjust(1)
    return builder.as_markup()