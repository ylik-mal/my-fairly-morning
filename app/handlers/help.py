from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "🌅 <b>My Fairly Morning — помощь</b>\n\n"
        "Бот для отслеживания привычек и вечерней рефлексии.\n\n"
        "📋 <b>Навигация:</b>\n"
        "/menu — интерактивное меню со всеми разделами\n"
        "/help — эта справка\n"
        "/start — перезапустить бота\n\n"
        "💡 <b>С чего начать:</b>\n"
        "1. Добавь привычку: <code>/add_habit Выпить воды</code>\n"
        "2. Настрой утренний дайджест: <code>/set_morning 08:00</code>\n"
        "3. Отмечай привычки каждый день: /today\n"
        "4. Вечером — рефлексия: /reflect\n\n"
        "📚 <b>Развитие:</b>\n"
        "/word — слово дня\n"
        "/topics — выбрать тему слов\n\n"
        "🥠 <b>Бонус:</b>\n"
        "/cookie — предсказание на день\n\n"
        "❓ Все остальные команды — в /menu\n"
        "Там разделы: Привычки, Напоминания, Рефлексия, Аналитика, Развитие."
    )