from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.csv_export import generate_habits_csv, generate_reflections_csv


router = Router()


def export_keyboard():
    """Клавиатура с выбором типа экспорта."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📋 Привычки", callback_data="export:habits")
    builder.button(text="📝 Рефлексии", callback_data="export:reflections")
    builder.adjust(2)
    return builder.as_markup()


@router.message(Command("export"))
async def cmd_export(message: Message) -> None:
    await message.answer(
        "📤 <b>Что экспортировать?</b>\n\n"
        "Выбери тип данных для скачивания в CSV:",
        reply_markup=export_keyboard(),
    )


@router.callback_query(F.data == "export:habits")
async def export_habits(callback: CallbackQuery) -> None:
    buffer = await generate_habits_csv(callback.from_user.id)

    if buffer is None:
        await callback.answer("У тебя нет привычек для экспорта", show_alert=True)
        return

    file = BufferedInputFile(
        buffer.read(),
        filename="habits.csv",
    )

    await callback.message.answer_document(
        document=file,
        caption="📋 <b>Твои привычки и статистика (30 дней)</b>",
    )
    await callback.answer()


@router.callback_query(F.data == "export:reflections")
async def export_reflections(callback: CallbackQuery) -> None:
    buffer = await generate_reflections_csv(callback.from_user.id)

    if buffer is None:
        await callback.answer("У тебя нет рефлексий для экспорта", show_alert=True)
        return

    file = BufferedInputFile(
        buffer.read(),
        filename="reflections.csv",
    )

    await callback.message.answer_document(
        document=file,
        caption="📝 <b>Твоя история рефлексий</b>",
    )
    await callback.answer()