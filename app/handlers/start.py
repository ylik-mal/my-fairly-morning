from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.db import get_or_create_user, get_user_habits, is_new_user


router = Router()


def welcome_keyboard():
    """Кнопки быстрого доступа для приветствия."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📋 Открыть меню", callback_data="menu:main")
    builder.button(text="➕ Добавить привычку", callback_data="welcome:add")
    builder.button(text="📋 Мои привычки", callback_data="welcome:list")
    builder.button(text="❓ Помощь", callback_data="welcome:help")
    builder.adjust(1)
    return builder.as_markup()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    first_time = await is_new_user(message.from_user.id)

    if first_time:
        text = (
            f"Привет, {message.from_user.first_name}! 🌅\n\n"
            "Я — бот <b>My Fairly Morning</b>.\n"
            "Помогаю выстроить утренние привычки и вести вечернюю рефлексию.\n\n"
            "📋 <b>Как начать:</b>\n\n"
            "<b>1.</b> Добавь первую привычку:\n"
            "   <code>/add_habit Выпить стакан воды</code>\n\n"
            "<b>2.</b> Настрой утренний дайджест:\n"
            "   <code>/set_morning 08:00</code>\n\n"
            "<b>3.</b> Отмечай привычки каждый день:\n"
            "   <code>/today</code>\n\n"
            "🌙 Вечером — рефлексия:\n"
            "   <code>/reflect</code> или <code>/set_evening 21:00</code>\n\n"
            "Все команды: /help\n\n"
            "Готов начать? Жми кнопку ниже 👇"
        )
    else:
        text = (
            f"С возвращением, {message.from_user.first_name}! 🌅\n\n"
            "Рад снова тебя видеть.\n\n"
            "<b>Быстрые команды:</b>\n"
            "/today — отметить привычки\n"
            "/my_habits — список привычек\n"
            "/stats — статистика за неделю\n"
            "/help — все команды"
        )

    await message.answer(text, reply_markup=welcome_keyboard())


@router.callback_query(F.data == "welcome:add")
async def welcome_add(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "➕ <b>Добавить привычку</b>\n\n"
        "Напиши команду в формате:\n"
        "<code>/add_habit Название привычки</code>\n\n"
        "Например:\n"
        "<code>/add_habit Выпить стакан воды</code>\n"
        "<code>/add_habit Сделать зарядку</code>"
    )
    await callback.answer()


@router.callback_query(F.data == "welcome:list")
async def welcome_list(callback: CallbackQuery) -> None:
    habits = await get_user_habits(callback.from_user.id)

    if not habits:
        await callback.message.answer(
            "📋 У тебя пока нет привычек.\n\n"
            "Добавь первую:\n"
            "<code>/add_habit Выпить воды</code>"
        )
    else:
        lines = [f"{i}. {title}" for i, (_, title) in enumerate(habits, start=1)]
        await callback.message.answer(
            "📋 <b>Твои привычки:</b>\n\n" + "\n".join(lines)
        )

    await callback.answer()


@router.callback_query(F.data == "welcome:help")
async def welcome_help(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "❓ Все команды: /help\n\n"
        "Или посмотри меню слева от поля ввода 👉"
    )
    await callback.answer()