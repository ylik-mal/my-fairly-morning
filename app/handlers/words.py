from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.db import get_word_topic, set_word_topic
from app.utils.words import TOPICS, get_word_of_the_day


router = Router()


def topics_keyboard():
    """Кнопки выбора темы."""
    builder = InlineKeyboardBuilder()
    for topic_key, topic_name in TOPICS.items():
        builder.button(text=topic_name, callback_data=f"topic:{topic_key}")
    builder.adjust(1)
    return builder.as_markup()


async def send_word(message: Message) -> None:
    """Отправляет слово дня из выбранной темы."""
    topic = await get_word_topic(message.from_user.id)
    word, data = get_word_of_the_day(topic)

    synonyms_line = " → ".join(data["synonyms"])
    english_line = " / ".join(data["english"])
    topic_name = TOPICS.get(topic, "🎭 Эмоции и чувства")

    await message.answer(
        f"📚 <b>Слово дня: {word.upper()}</b>\n"
        f"<i>Тема: {topic_name}</i>\n\n"
        f"• {synonyms_line}\n\n"
        f"🇬🇧 {english_line}"
    )


@router.message(Command("word"))
async def cmd_word(message: Message) -> None:
    await send_word(message)


@router.message(Command("topics"))
async def cmd_topics(message: Message) -> None:
    await message.answer(
        "📚 <b>Выбери тему для слова дня:</b>\n\n"
        "Бот будет присылать слова из этой темы.",
        reply_markup=topics_keyboard(),
    )


@router.callback_query(F.data.startswith("topic:"))
async def on_topic_select(callback: CallbackQuery) -> None:
    topic = callback.data.split(":")[1]
    await set_word_topic(callback.from_user.id, topic)

    topic_name = TOPICS.get(topic, topic)
    await callback.answer(f"Тема: {topic_name}")

    await callback.message.edit_text(
        f"✅ Тема установлена: <b>{topic_name}</b>\n\n"
        "Теперь /word будет присылать слова из этой темы."
    )