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
        "character": {
        "добрый": {
            "synonyms": ["добрый", "сердечный", "душевный", "милосердный", "великодушный"],
            "english": ["kind", "warm", "caring", "compassionate", "magnanimous"],
        },
        "смелый": {
            "synonyms": ["смелый", "храбрый", "отважный", "бесстрашный", "дерзновенный"],
            "english": ["brave", "bold", "courageous", "fearless", "audacious"],
        },
        "честный": {
            "synonyms": ["честный", "правдивый", "открытый", "неподкупный", "безупречный"],
            "english": ["honest", "truthful", "frank", "incorruptible", "upright"],
        },
        "скромный": {
            "synonyms": ["скромный", "сдержанный", "застенчивый", "непритязательный", "деликатный"],
            "english": ["modest", "humble", "reserved", "unassuming", "reticent"],
        },
        "гордый": {
            "synonyms": ["гордый", "величавый", "величественный", "надменный", "непреклонный"],
            "english": ["proud", "majestic", "dignified", "lofty", "imperious"],
        },
        "упрямый": {
            "synonyms": ["упрямый", "настойчивый", "непреклонный", "неподатливый", "неуступчивый"],
            "english": ["stubborn", "persistent", "adamant", "obstinate", "unyielding"],
        },
        "ленивый": {
            "synonyms": ["ленивый", "праздный", "неповоротливый", "бездеятельный", "расслабленный"],
            "english": ["lazy", "idle", "sluggish", "inactive", "indolent"],
        },
        "щедрый": {
            "synonyms": ["щедрый", "великодушный", "благородный", "расточительный", "безмерный"],
            "english": ["generous", "openhanded", "bountiful", "lavish", "magnanimous"],
        },
        "искренний": {
            "synonyms": ["искренний", "открытый", "чистосердечный", "правдивый", "неподдельный"],
            "english": ["sincere", "open", "genuine", "honest", "heartfelt"],
        },
        "застенчивый": {
            "synonyms": ["застенчивый", "робкий", "стеснительный", "неуверенный", "стыдливый"],
            "english": ["shy", "timid", "bashful", "diffident", "self-conscious"],
        },
        "уверенный": {
            "synonyms": ["уверенный", "твёрдый", "решительный", "несомненный", "бесспорный"],
            "english": ["confident", "assured", "certain", "determined", "unwavering"],
        },
        "надёжный": {
            "synonyms": ["надёжный", "верный", "проверенный", "прочный", "непоколебимый"],
            "english": ["reliable", "trustworthy", "dependable", "solid", "steadfast"],
        },
        "терпеливый": {
            "synonyms": ["терпеливый", "выдержанный", "спокойный", "кроткий", "снисходительный"],
            "english": ["patient", "forbearing", "tolerant", "enduring", "long-suffering"],
        },
        "трудолюбивый": {
            "synonyms": ["трудолюбивый", "работящий", "усердный", "прилежный", "старательный"],
            "english": ["hardworking", "industrious", "diligent", "assiduous", "studious"],
        },
        "внимательный": {
            "synonyms": ["внимательный", "заботливый", "чуткий", "предупредительный", "участливый"],
            "english": ["attentive", "caring", "considerate", "thoughtful", "mindful"],
        },
        "отзывчивый": {
            "synonyms": ["отзывчивый", "чуткий", "внимательный", "сердечный", "сочувствующий"],
            "english": ["responsive", "sympathetic", "kind", "considerate", "warmhearted"],
        },
        "справедливый": {
            "synonyms": ["справедливый", "беспристрастный", "объективный", "непредвзятый", "честный"],
            "english": ["fair", "just", "impartial", "objective", "equitable"],
        },
        "великодушный": {
            "synonyms": ["великодушный", "благородный", "щедрый", "милосердный", "возвышенный"],
            "english": ["magnanimous", "noble", "generous", "forgiving", "bighearted"],
        },
        "решительный": {
            "synonyms": ["решительный", "твёрдый", "напористый", "смелый", "бескомпромиссный"],
            "english": ["decisive", "resolute", "determined", "firm", "uncompromising"],
        },
        "спокойный": {
            "synonyms": ["спокойный", "уравновешенный", "невозмутимый", "хладнокровный", "сдержанный"],
            "english": ["calm", "poised", "composed", "level-headed", "unflappable"],
        },
        "общительный": {
            "synonyms": ["общительный", "компанейский", "дружелюбный", "открытый", "разговорчивый"],
            "english": ["sociable", "outgoing", "friendly", "gregarious", "talkative"],
        },
        "замкнутый": {
            "synonyms": ["замкнутый", "нелюдимый", "скрытный", "отчуждённый", "уединённый"],
            "english": ["reserved", "withdrawn", "introverted", "aloof", "solitary"],
        },
        "любознательный": {
            "synonyms": ["любознательный", "пытливый", "любопытный", "дотошный", "исследовательский"],
            "english": ["curious", "inquisitive", "eager to learn", "probing", "exploratory"],
        },
        "мудрый": {
            "synonyms": ["мудрый", "разумный", "глубокий", "прозорливый", "просветлённый"],
            "english": ["wise", "prudent", "profound", "insightful", "enlightened"],
        },
        "проницательный": {
            "synonyms": ["проницательный", "прозорливый", "зоркий", "дальновидный", "глубокий"],
            "english": ["insightful", "perceptive", "astute", "discerning", "sharp"],
        },
        "энергичный": {
            "synonyms": ["энергичный", "деятельный", "активный", "живой", "стремительный"],
            "english": ["energetic", "active", "dynamic", "lively", "vigorous"],
        },
        "флегматичный": {
            "synonyms": ["флегматичный", "невозмутимый", "спокойный", "уравновешенный", "медлительный"],
            "english": ["phlegmatic", "calm", "placid", "unemotional", "impassive"],
        },
        "вспыльчивый": {
            "synonyms": ["вспыльчивый", "горячий", "несдержанный", "импульсивный", "запальчивый"],
            "english": ["hot-tempered", "irascible", "impulsive", "quick-tempered", "fiery"],
        },
        "обаятельный": {
            "synonyms": ["обаятельный", "очаровательный", "привлекательный", "шармирующий", "магнетический"],
            "english": ["charming", "captivating", "alluring", "magnetic", "charismatic"],
        },
        "скрупулёзный": {
            "synonyms": ["скрупулёзный", "педантичный", "тщательный", "дотошный", "аккуратный"],
            "english": ["meticulous", "scrupulous", "thorough", "painstaking", "precise"],
        },
        "принципиальный": {
            "synonyms": ["принципиальный", "твёрдый", "непреклонный", "честный", "порядочный"],
            "english": ["principled", "firm", "resolute", "honest", "moral"],
        },
        "самоуверенный": {
            "synonyms": ["самоуверенный", "самодовольный", "надменный", "самонадеянный", "спесивый"],
            "english": ["overconfident", "smug", "arrogant", "presumptuous", "haughty"],
        },
    },
        "nature": {
        "солнце": {
            "synonyms": ["солнце", "светило", "звезда", "лучезарное светило", "дневное светило"],
            "english": ["sun", "sunshine", "daystar", "orb", "luminary"],
        },
        "дождь": {
            "synonyms": ["дождь", "ливень", "морось", "гроза", "непогода"],
            "english": ["rain", "shower", "drizzle", "downpour", "storm"],
        },
        "ветер": {
            "synonyms": ["ветер", "ветерок", "вихрь", "буря", "ураган"],
            "english": ["wind", "breeze", "gust", "storm", "hurricane"],
        },
        "снег": {
            "synonyms": ["снег", "пороша", "снежок", "пурга", "метель"],
            "english": ["snow", "snowfall", "snowflake", "blizzard", "snowstorm"],
        },
        "туман": {
            "synonyms": ["туман", "мгла", "дымка", "марево", "пелена"],
            "english": ["fog", "mist", "haze", "vapor", "cloud"],
        },
        "рассвет": {
            "synonyms": ["рассвет", "заря", "восход", "утренняя заря", "первый свет"],
            "english": ["dawn", "sunrise", "daybreak", "morning", "first light"],
        },
        "закат": {
            "synonyms": ["закат", "заход", "вечерняя заря", "сумерки", "закатная пора"],
            "english": ["sunset", "dusk", "twilight", "evening", "sundown"],
        },
        "тишина": {
            "synonyms": ["тишина", "тишь", "молчание", "безмолвие", "покой"],
            "english": ["silence", "stillness", "quiet", "calm", "hush"],
        },
        "гроза": {
            "synonyms": ["гроза", "буря", "непогода", "шторм", "ненастье"],
            "english": ["thunderstorm", "storm", "tempest", "squall", "gale"],
        },
        "радуга": {
            "synonyms": ["радуга", "дуга", "разноцветная полоса", "семицветье", "небесный мост"],
            "english": ["rainbow", "arc", "arch", "spectrum", "prism"],
        },
        "зимний": {
            "synonyms": ["зимний", "морозный", "студёный", "холодный", "ледяной"],
            "english": ["winter", "frosty", "chilly", "icy", "snowy"],
        },
        "весенний": {
            "synonyms": ["весенний", "апрельский", "цветущий", "свежий", "первоцветный"],
            "english": ["spring", "vernal", "blooming", "fresh", "budding"],
        },
        "осенний": {
            "synonyms": ["осенний", "золотой", "унылый", "дождливый", "промозглый"],
            "english": ["autumn", "fall", "golden", "rainy", "damp"],
        },
        "летний": {
            "synonyms": ["летний", "жаркий", "знойный", "солнечный", "тёплый"],
            "english": ["summer", "hot", "sunny", "warm", "sultry"],
        },
        "свежий": {
            "synonyms": ["свежий", "прохладный", "бодрящий", "чистый", "живительный"],
            "english": ["fresh", "cool", "crisp", "bracing", "refreshing"],
        },
        "тёплый": {
            "synonyms": ["тёплый", "мягкий", "ласковый", "уютный", "согревающий"],
            "english": ["warm", "mild", "gentle", "cozy", "balmy"],
        },
        "прохладный": {
            "synonyms": ["прохладный", "свежий", "холодноватый", "студёный", "бодрящий"],
            "english": ["cool", "chilly", "fresh", "crisp", "brisk"],
        },
        "пасмурный": {
            "synonyms": ["пасмурный", "хмурый", "облачный", "серый", "угрюмый"],
            "english": ["gloomy", "overcast", "cloudy", "gray", "dreary"],
        },
        "ясный": {
            "synonyms": ["ясный", "солнечный", "прозрачный", "чистый", "безоблачный"],
            "english": ["clear", "sunny", "bright", "cloudless", "fair"],
        },
        "солнечный": {
            "synonyms": ["солнечный", "светлый", "лучезарный", "тёплый", "золотой"],
            "english": ["sunny", "bright", "radiant", "warm", "golden"],
        },
        "звёздный": {
            "synonyms": ["звёздный", "ночной", "небесный", "мерцающий", "сияющий"],
            "english": ["starry", "nightly", "celestial", "twinkling", "gleaming"],
        },
        "лунный": {
            "synonyms": ["лунный", "лучезарный", "серебристый", "бледный", "сияющий"],
            "english": ["lunar", "moonlit", "silvery", "pale", "glowing"],
        },
        "утренний": {
            "synonyms": ["утренний", "ранний", "рассветный", "бодрый", "свежий"],
            "english": ["morning", "early", "dawning", "fresh", "matutinal"],
        },
        "вечерний": {
            "synonyms": ["вечерний", "закатный", "сумеречный", "тихий", "уютный"],
            "english": ["evening", "twilight", "dusky", "quiet", "vespertine"],
        },
        "ночной": {
            "synonyms": ["ночной", "тёмный", "звёздный", "лунный", "таинственный"],
            "english": ["night", "dark", "nocturnal", "starry", "mysterious"],
        },
        "река": {
            "synonyms": ["река", "речка", "поток", "русло", "водная артерия"],
            "english": ["river", "stream", "flow", "waterway", "current"],
        },
        "море": {
            "synonyms": ["море", "океан", "пучина", "глубь", "водная гладь"],
            "english": ["sea", "ocean", "deep", "expanse", "waters"],
        },
        "лес": {
            "synonyms": ["лес", "чаща", "роща", "бор", "дубрава"],
            "english": ["forest", "wood", "grove", "thicket", "woodland"],
        },
        "поле": {
            "synonyms": ["поле", "луг", "равнина", "пашня", "простор"],
            "english": ["field", "meadow", "plain", "grassland", "expanse"],
        },
        "гора": {
            "synonyms": ["гора", "вершина", "пик", "хребет", "круча"],
            "english": ["mountain", "peak", "summit", "ridge", "height"],
        },
    },
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