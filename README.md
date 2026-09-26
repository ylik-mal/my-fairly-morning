# My Fairly Morning 🌅
Telegram-бот для хорошего начала дня, отслеживания привычек и саморефлексии.

## Возможности
- ✅ Добавление привычек (`/add_habit`)
- ✅ Просмотр списка привычек (`/my_habits`)
- 🚧 Утренний чек-лист привычек (в разработке)
- 📅 Вечерняя рефлексия
- 📅 Визуализация прогресса
- 📅 Бонус (печенька с предсказанием)

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

## Текущий статус

- ✅ Foundation (aiogram, /start)
- ✅ SQLite database (users, habits)
- 🚧 Commands for habits (in progress)
- 📅 Reminders, statistics, charts