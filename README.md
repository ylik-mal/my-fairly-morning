# My Fairly Morning 🌅

Telegram-бот для хорошего начала дня, отслеживания привычек и саморефлексии.

## Возможности
- Утренний чек-лист привычек
- Вечерняя рефлексия
- Визуализация прогресса
- бонус (ввиде печеньки с предсказанием)

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