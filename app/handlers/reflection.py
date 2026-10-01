from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from app.database.db import get_recent_reflections, save_reflection


router = Router()


class Reflection(StatesGroup):
    waiting_rating = State()
    waiting_success = State()
    waiting_failure = State()


@router.message(Command("reflect"))
async def cmd_reflect(message: Message, state: FSMContext) -> None:
    await state.set_state(Reflection.waiting_rating)
    await state.update_data(rating=None, success=None, failure=None)
    await message.answer(
        "🌙 <b>Вечерняя рефлексия</b>\n\n"
        "Шаг 1/3: Оцени день от 1 до 10."
    )


@router.message(Reflection.waiting_rating)
async def process_rating(message: Message, state: FSMContext) -> None:
    text = message.text.strip()

    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer(
            "Пожалуйста, введи число от 1 до 10."
        )
        return

    await state.update_data(rating=int(text))
    await state.set_state(Reflection.waiting_success)
    await message.answer(
        "Шаг 2/3: Что сегодня удалось?"
    )


@router.message(Reflection.waiting_success)
async def process_success(message: Message, state: FSMContext) -> None:
    text = message.text.strip()
    if not text:
        await message.answer("Напиши что-нибудь.")
        return

    await state.update_data(success=text)
    await state.set_state(Reflection.waiting_failure)
    await message.answer(
        "Шаг 3/3: Что не получилось?"
    )


@router.message(Reflection.waiting_failure)
async def process_failure(message: Message, state: FSMContext) -> None:
    text = message.text.strip()
    if not text:
        await message.answer("Напиши что-нибудь.")
        return

    data = await state.get_data()
    await save_reflection(
        user_id=message.from_user.id,
        rating=data.get("rating"),
        success=data.get("success"),
        failure=text,
    )

    await state.clear()
    await message.answer(
        "✅ <b>Спасибо! Рефлексия сохранена.</b>\n\n"
        "Посмотреть историю: /my_reflections (скоро)"
    )
@router.message(Command("my_reflections"))
async def cmd_my_reflections(message: Message) -> None:
    reflections = await get_recent_reflections(message.from_user.id, limit=7)

    if not reflections:
        await message.answer(
            "У тебя пока нет рефлексий.\n\n"
            "Начни первую: /reflect"
        )
        return

    lines = ["📓 <b>Последние рефлексии:</b>\n"]

    for date_str, rating, success, failure in reflections:
        # date_str в формате 2026-09-30 → 30.09.2026
        year, month, day = date_str.split("-")
        pretty_date = f"{day}.{month}.{year}"

        rating_str = f"{rating}/10" if rating is not None else "—"
        success_str = success or "—"
        failure_str = failure or "—"

        lines.append(
            f"📅 <b>{pretty_date}</b> — Оценка: {rating_str}\n"
            f"✅ Удалось: {success_str}\n"
            f"❌ Не получилось: {failure_str}\n"
        )

    await message.answer("\n".join(lines))