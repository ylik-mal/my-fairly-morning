[![Tests](https://github.com/ylik-mal/my-fairly-morning/actions/workflows/tests.yml/badge.svg)](https://github.com/ylik-mal/my-fairly-morning/actions/workflows/tests.yml)

# My Fairly Morning 🌅

Telegram-бот для отслеживания привычек и вечерней рефлексии.

<p align="center">
  <img src="docs/screenshots/02_start.jpg" width="280" alt="Старт"/>
  <img src="docs/screenshots/03_today.jpg" width="280" alt="Сегодня"/>
</p>

<p align="center">
  <img src="docs/screenshots/04_chart.jpg" width="500" alt="График"/>
</p>

## Возможности

- ✅ Добавление привычек (`/add_habit`)
- ✅ Просмотр списка привычек (`/my_habits`)
- ✅ Ежедневные отметки (`/today` с кнопками «Сделано / Пропустить»)
- ✅ Утренний дайджест (`/set_morning HH:MM`)
- ✅ Вечерняя рефлексия (FSM-диалог, `/reflect`)
- ✅ История рефлексий (`/my_reflections`)
- ✅ Статистика за 7 дней (`/stats`)
- ✅ Графики выполнения (`/chart`)
- ✅ Интерактивное меню (`/menu` с разделами)
- ✅ Слово дня с 5 темами (`/word`, `/topics`)
- ✅ Тематические синонимы и английские переводы
- ✅ Ежедневная печенька с мотивацией (`/cookie`)
- ✅ Утренний дайджест с привычками, словом дня и печенькой

## Меню команд

<p align="center">
  <img src="docs/screenshots/01_menu.jpg" width="300" alt="Меню"/>
</p>

## Стек

- Python 3.12
- aiogram 3.x
- SQLite (aiosqlite)
- APScheduler
- matplotlib
- pytest + pytest-asyncio
- GitHub Actions (CI)


## Слово дня

Бот присылает одно слово в день из выбранной темы — с синонимами (от простого к сложному) и английскими переводами.

### Доступные темы

- 🎭 Эмоции и чувства — 29 слов
- 💪 Характер человека — 32 слова
- 🌿 Природа и погода — 30 слов
- 🧠 Мышление и интеллект — 30 слов
- ✨ Красота и эстетика — 30 слов

**Всего: 151 слово.** Смена темы: `/topics`.

### Пример
📚 Слово дня: КРАСИВЫЙ

• красивый → милый → пригожий → живописный → великолепный → божественный

🇬🇧 beautiful / pretty / handsome / picturesque / magnificent / gorgeous


## Печенька с предсказанием

Команда `/cookie` присылает случайное мотивационное предсказание из 30 фраз. Печенька автоматически добавляется в утренний дайджест.

### Пример
🥠 Твоё предсказание на сегодня:

«Сегодня отличный день, чтобы начать что-то новое.
Не откладывай мечты — сделай первый шаг!»

🍀 Удачного дня!

## Установка

### Требования
- Python 3.12
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

### Шаги

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/ylik-mal/my-fairly-morning.git
   cd my-fairly-morning