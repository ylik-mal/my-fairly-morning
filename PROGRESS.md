# Progress Tracker

**Дедлайн:** 20 декабря 2026
**Старт:** 23 сентября 2026
**Цель:** 70 дней активности

## Текущий статус

- **День:** 45 / 70 (64% complete)
- **Коммитов:** ~80
- **Календарных дней до дедлайна:** 44
- **Буфер отдыха:** 5 дней

## Что работает

- ✅ Telegram-бот на aiogram 3.x
- ✅ SQLite (users, habits, checkins, user_settings, reflections, user_word_topic)
- ✅ 17 команд: /start, /help, /menu, /add_habit, /my_habits, /today,
   /set_morning, /morning, /set_evening, /evening,
   /reflect, /my_reflections, /stats, /chart, /word, /topics, /cookie, /export
- ✅ Утренний дайджест (APScheduler)
- ✅ Вечерняя рефлексия с FSM-диалогом
- ✅ Инлайн-кнопки в /today
- ✅ Графики matplotlib
- ✅ Онбординг-туториал в /start
- ✅ Меню команд с эмодзи
- ✅ README со скриншотами, архитектурой и блоками кода
- ✅ 5 тем слов (151 слово)
- ✅ CSV-экспорт для Excel
- ✅ Streak (серия дней)
- ✅ Docker configuration
- ✅ DEPLOY.md инструкция для VPS
- ✅ 21 тест (pytest)
- ✅ GitHub Actions (CI)
- ✅ Docstrings для всего кода (db, utils, handlers)

## План по неделям

| Неделя | Период | Цель | Статус |
|--------|--------|------|--------|
| 1 | 23.09–29.09 | Foundation, БД, /start | ✅ |
| 2 | 30.09–06.10 | Рефлексия, статистика, графики | ✅ |
| 3 | 07.10–13.10 | Тесты, CI, /menu | ✅ |
| 4 | 14.10–20.10 | 5 тем слов, /cookie, streak | ✅ |
| 5 | 21.10–27.10 | CSV, Docker, README | ✅ |
| 6 | 28.10–03.11 | Тесты export/cookie, /start | ✅ |
| 7 | 04.11–10.11 | Документация (API, docstrings) | ✅ |
| 8 | 11.11–17.11 | Deploy на VPS | 🚧 |
| 9 | 18.11–24.11 | CI/CD auto-deploy | 📅 |
| 10 | 25.11–20.12 | Полировка, GIF, презентация | 📅 |

## Что дальше

- [ ] Деплой на VPS (бюджет: 200–460 ₽/мес)
- [ ] Настройка Outline VPN или SOCKS5 на сервере (если VPS в РФ)
- [ ] Проверка работы бота 24/7
- [ ] GIF-демо для README
- [ ] Презентация проекта