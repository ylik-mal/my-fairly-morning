from datetime import date, timedelta

import pytest

from app.utils.words import TOPICS, WORDS_BY_TOPIC, get_word_of_the_day


def test_all_topics_have_words():
    """Каждая тема должна содержать хотя бы 25 слов."""
    for topic in TOPICS:
        assert topic in WORDS_BY_TOPIC, f"Тема '{topic}' отсутствует в WORDS_BY_TOPIC"
        words = WORDS_BY_TOPIC[topic]
        assert len(words) >= 25, f"В теме '{topic}' только {len(words)} слов (нужно ≥25)"


def test_every_word_has_synonyms_and_english():
    """У каждого слова должны быть synonyms и english."""
    for topic, words in WORDS_BY_TOPIC.items():
        for word, data in words.items():
            assert "synonyms" in data, f"У слова '{word}' ({topic}) нет synonyms"
            assert "english" in data, f"У слова '{word}' ({topic}) нет english"
            assert len(data["synonyms"]) >= 3, f"У '{word}' мало синонимов"
            assert len(data["english"]) >= 3, f"У '{word}' мало английских слов"


def test_get_word_of_the_day_stable():
    """Для одной и той же даты — одно и то же слово."""
    test_date = date(2026, 10, 14)

    word1, data1 = get_word_of_the_day("emotions", test_date)
    word2, data2 = get_word_of_the_day("emotions", test_date)

    assert word1 == word2
    assert data1 == data2


def test_get_word_of_the_day_changes_by_date():
    """Слова меняются со временем."""
    day1 = date(2026, 10, 14)

    words = set()
    for i in range(5):
        d = day1 + timedelta(days=i)
        w, _ = get_word_of_the_day("emotions", d)
        words.add(w)

    assert len(words) >= 2, "За 5 дней слово ни разу не сменилось"


def test_get_word_of_the_day_unknown_topic():
    """Если тема неизвестна — возвращается слово из emotions."""
    test_date = date(2026, 10, 14)

    word_unknown, _ = get_word_of_the_day("unknown_topic", test_date)
    word_emotions, _ = get_word_of_the_day("emotions", test_date)

    assert word_unknown == word_emotions


def test_all_topics_return_valid_word():
    """Каждая тема возвращает корректное слово с данными."""
    test_date = date(2026, 10, 14)

    for topic in TOPICS:
        word, data = get_word_of_the_day(topic, test_date)
        assert word, f"Пустое слово для темы '{topic}'"
        assert "synonyms" in data, f"Нет synonyms для '{topic}'"
        assert "english" in data, f"Нет english для '{topic}'"