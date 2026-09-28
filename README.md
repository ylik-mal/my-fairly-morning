# My Fairly Morning 🌅
Telegram-бот для хорошего начала дня, отслеживания привычек и саморефлексии.

## Возможности

- ✅ Добавление привычек (`/add_habit`)
- ✅ Просмотр списка привычек (`/my_habits`)
- ✅ Ежедневные отметки (`/today` с кнопками)
- ✅ Утренний дайджест (`/set_morning HH:MM`)
- 🚧 Вечерняя рефлексия (в разработке)
- 📅 Статистика и графики

## Стек
- Python 3.12
- aiogram 3.x
- SQLite
- matplotlib

## Запуск
(будет добавлено позже)

## Roadmap
See [ROADMAP.md](ROADMAP.md) for the development plan.

## Работа через прокси
В регионах, где `api.telegram.org` недоступен, бот поддерживает работу через SOCKS5-прокси. Укажите прокси в `main.py`:

```python
session = AiohttpSession(proxy="socks5://IP:PORT")

### Текущий статус

- ✅ Foundation (aiogram, `/start`)
- ✅ SQLite database (users, habits, checkins, user_settings)
- ✅ Habit management (`/add_habit`, `/my_habits`)
- ✅ Daily check-ins (`/today` with inline buttons)
- ✅ Morning digest (APScheduler, `/set_morning`)
- 🚧 Evening reflection (in progress)
- 📅 Statistics, charts, deployment (planned)