from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "🌅 <b>My Fairly Morning — помощь</b>\n\n"
        "📋 <b>Привычки:</b>\n"
        "/add_habit <i>Название</i> — добавить привычку\n"
        "/my_habits — список привычек\n"
        "/today — отметить привычки на сегодня\n\n"
        "⏰ <b>Напоминания:</b>\n"
        "/set_morning <i>HH:MM</i> — время утреннего дайджеста\n"
        "/morning — текущее время дайджеста\n\n"
        "🌙 <b>Рефлексия:</b>\n"
        "/reflect — начать вечернюю рефлексию\n"
        "/set_evening <i>HH:MM</i> — время вечернего опроса\n"
        "/evening — текущее время опроса\n"
        "/my_reflections — история рефлексий\n\n"
        "ℹ️ <b>Прочее:</b>\n"
        "/help — эта справка\n"
        "/start — перезапустить бота"
    )