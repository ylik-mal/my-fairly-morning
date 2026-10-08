from datetime import date


TOPICS = {
    "emotions": "🎭 Эмоции и чувства",
    "character": "💪 Характер человека",
    "nature": "🌿 Природа и погода",
    "mind": "🧠 Мышление и интеллект",
    "beauty": "✨ Красота и эстетика",
}


WORDS_BY_TOPIC = {
    "emotions": {
        "радость": {
            "synonyms": ["радость", "веселье", "ликование", "восторг", "упоение"],
            "english": ["joy", "delight", "elation", "exultation", "ecstasy"],
        },
        "грусть": {
            "synonyms": ["грусть", "печаль", "тоска", "уныние", "скорбь"],
            "english": ["sadness", "sorrow", "melancholy", "gloom", "grief"],
        },
        "страх": {
            "synonyms": ["страх", "боязнь", "тревога", "ужас", "паника"],
            "english": ["fear", "dread", "anxiety", "terror", "panic"],
        },
        "гнев": {
            "synonyms": ["гнев", "злость", "ярость", "негодование", "бешенство"],
            "english": ["anger", "rage", "fury", "indignation", "wrath"],
        },
        "любовь": {
            "synonyms": ["любовь", "привязанность", "нежность", "страсть", "обожание"],
            "english": ["love", "affection", "tenderness", "passion", "adoration"],
        },
        "спокойствие": {
            "synonyms": ["спокойствие", "умиротворение", "тишина", "безмятежность", "невозмутимость"],
            "english": ["calm", "serenity", "tranquility", "peace", "composure"],
        },
        "удивление": {
            "synonyms": ["удивление", "изумление", "поражение", "ошеломление", "потрясение"],
            "english": ["surprise", "astonishment", "amazement", "shock", "bewilderment"],
        },
        "стыд": {
            "synonyms": ["стыд", "смущение", "неловкость", "застенчивость", "конфуз"],
            "english": ["shame", "embarrassment", "awkwardness", "bashfulness", "confusion"],
        },
        "надежда": {
            "synonyms": ["надежда", "ожидание", "упование", "вера", "предвкушение"],
            "english": ["hope", "expectation", "anticipation", "faith", "optimism"],
        },
        "вдохновение": {
            "synonyms": ["вдохновение", "подъём", "воодушевление", "озарение", "муза"],
            "english": ["inspiration", "uplift", "enthusiasm", "enlightenment", "muse"],
        },
        "умиротворение": {
            "synonyms": ["умиротворение", "спокойствие", "тишина", "безмятежность", "успокоение"],
            "english": ["serenity", "peace", "tranquility", "calmness", "placidity"],
        },
        "ностальгия": {
            "synonyms": ["ностальгия", "тоска", "грусть", "память", "воспоминание"],
            "english": ["nostalgia", "longing", "yearning", "reminiscence", "homesickness"],
        },
        "восхищение": {
            "synonyms": ["восхищение", "восторг", "изумление", "преклонение", "обожание"],
            "english": ["admiration", "delight", "awe", "reverence", "adoration"],
        },
        "тревога": {
            "synonyms": ["тревога", "беспокойство", "волнение", "опасение", "паника"],
            "english": ["anxiety", "worry", "unease", "apprehension", "alarm"],
        },
        "уверенность": {
            "synonyms": ["уверенность", "спокойствие", "решимость", "твёрдость", "убеждённость"],
            "english": ["confidence", "assurance", "certainty", "conviction", "poise"],
        },
        "сочувствие": {
            "synonyms": ["сочувствие", "сопереживание", "эмпатия", "сострадание", "участие"],
            "english": ["compassion", "empathy", "sympathy", "understanding", "pity"],
        },
        "зависть": {
            "synonyms": ["зависть", "ревность", "досада", "огорчение", "недовольство"],
            "english": ["envy", "jealousy", "resentment", "grudge", "covetousness"],
        },
        "благодарность": {
            "synonyms": ["благодарность", "признательность", "ценность", "уважение", "почитание"],
            "english": ["gratitude", "thankfulness", "appreciation", "recognition", "acknowledgment"],
        },
        "одиночество": {
            "synonyms": ["одиночество", "уединение", "изоляция", "отчуждение", "покинутость"],
            "english": ["loneliness", "solitude", "isolation", "seclusion", "estrangement"],
        },
        "восторг": {
            "synonyms": ["восторг", "ликование", "упоение", "экстаз", "восхищение"],
            "english": ["delight", "rapture", "ecstasy", "bliss", "elation"],
        },
        "нежность": {
            "synonyms": ["нежность", "ласка", "мягкость", "трепетность", "чуткость"],
            "english": ["tenderness", "gentleness", "affection", "softness", "fondness"],
        },
        "трепет": {
            "synonyms": ["трепет", "волнение", "благоговение", "робость", "смущение"],
            "english": ["trepidation", "awe", "trepidity", "timidity", "shyness"],
        },
        "азарт": {
            "synonyms": ["азарт", "задор", "увлечение", "запал", "страсть"],
            "english": ["excitement", "zeal", "passion", "fervor", "enthusiasm"],
        },
        "апатия": {
            "synonyms": ["апатия", "безразличие", "равнодушие", "вялость", "безучастие"],
            "english": ["apathy", "indifference", "listlessness", "lethargy", "detachment"],
        },
        "уныние": {
            "synonyms": ["уныние", "тоска", "печаль", "подавленность", "меланхолия"],
            "english": ["despondency", "gloom", "melancholy", "dejection", "depression"],
        },
        "взволнованность": {
            "synonyms": ["взволнованность", "волнение", "возбуждение", "тревога", "ажитация"],
            "english": ["agitation", "excitement", "anxiety", "perturbation", "fluster"],
        },
        "упоение": {
            "synonyms": ["упоение", "восторг", "экстаз", "наслаждение", "блаженство"],
            "english": ["rapture", "ecstasy", "bliss", "delight", "euphoria"],
        },
        "смятение": {
            "synonyms": ["смятение", "растерянность", "замешательство", "смущение", "суматоха"],
            "english": ["confusion", "bewilderment", "perplexity", "disarray", "turmoil"],
        },
        "просветление": {
            "synonyms": ["просветление", "озарение", "понимание", "пробуждение", "ясность"],
            "english": ["enlightenment", "illumination", "realization", "awakening", "clarity"],
        },
    },
    "character": {},
    "nature": {},
    "mind": {},
    "beauty": {},
}


def get_word_of_the_day(topic: str, for_date: date | None = None) -> tuple[str, dict]:
    """Возвращает слово дня из указанной темы."""
    if for_date is None:
        for_date = date.today()

    words = WORDS_BY_TOPIC.get(topic) or WORDS_BY_TOPIC["emotions"]

    if not words:
        words = WORDS_BY_TOPIC["emotions"]

    words_list = list(words.items())
    day_of_year = for_date.timetuple().tm_yday
    index = day_of_year % len(words_list)

    return words_list[index]