# My Fairly Morning 🌅

Telegram-бот для отслеживания привычек и вечерней рефлексии.

<p align="center">
  <img src="docs/screenshots/02_start.png" width="300" alt="Старт"/>
  <img src="docs/screenshots/03_today.png" width="300" alt="Сегодня"/>
</p>

<p align="center">
  <img src="docs/screenshots/04_chart.png" width="500" alt="График"/>
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

## Меню команд

<p align="center">
  <img src="docs/screenshots/01_menu.png" width="300" alt="Меню"/>
</p>

## Стек

- Python 3.12
- aiogram 3.x
- SQLite (aiosqlite)
- APScheduler
- matplotlib

## Установка

### Требования
- Python 3.12
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

### Шаги

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/ylik-mal/my-fairly-morning.git
   cd my-fairly-morning