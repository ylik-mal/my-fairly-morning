# Roadmap — My Fairly Morning 🌅

План развития проекта на 10 недель (23.09.2026 – 20.12.2026).

## ✅ Week 1 — Foundation (23.09–29.09)

- [x] Project structure and Git setup
- [x] aiogram 3 + bot initialization
- [x] `/start` command handler
- [x] SQLite database module
- [x] SOCKS5 proxy support

## ✅ Week 2 — Database & Habits (30.09–06.10)

- [x] `users` and `habits` tables
- [x] `/add_habit`, `/my_habits`, `/delete_habit`
- [x] `checkins` table + `/today` with inline buttons
- [x] APScheduler — morning digest
- [x] FSM-dialogue for evening reflection
- [x] `/set_morning`, `/set_evening`

## ✅ Week 3 — Quality (07.10–13.10)

- [x] pytest tests (14 tests: database + words)
- [x] GitHub Actions CI
- [x] `/menu` with sectioned navigation
- [x] `/help` — full command reference

## ✅ Week 4 — Content (14.10–20.10)

- [x] 5 word topics (151 words total)
- [x] `/word`, `/topics` with topic selection
- [x] `/cookie` — daily motivational fortune
- [x] Cookie in morning digest
- [x] Streak calculation in `/stats`

## ✅ Week 5 — Export & Docker (21.10–27.10)

- [x] CSV export (`/export` — habits and reflections)
- [x] Docker configuration
- [x] README with screenshots
- [x] PROGRESS.md tracker

## 🚧 Week 6 — Testing & Polish (28.10–03.11)

- [ ] Tests for `/export` and `/cookie`
- [ ] UX polish: truncate long titles in `/today` ✅
- [ ] Update `/start` with new features
- [ ] README: add code blocks for examples
- [ ] Fix duplicates in README

## 📅 Week 7 — Documentation (04.11–10.11)

- [ ] Complete API documentation in code
- [ ] Docstrings for all public functions
- [ ] Update ROADMAP with final results
- [ ] Add more screenshots

## 📅 Week 8 — Deployment (11.11–17.11)

- [ ] Buy VPS
- [ ] Setup Outline VPN (or paid SOCKS5)
- [ ] Deploy bot to VPS with Docker
- [ ] Verify 24/7 operation
- [ ] Setup auto-restart

## 📅 Week 9 — CI/CD (18.11–24.11)

- [ ] GitHub Actions: auto-deploy
- [ ] Tests coverage report
- [ ] Logging improvements
- [ ] Error monitoring

## 📅 Week 10 — Final (25.11–20.12)

- [ ] Final README polish
- [ ] Demo GIF / video
- [ ] Presentation for teacher
- [ ] Project defense
- [ ] 70 days of activity confirmed

## 📊 Current Status

**Day:** 31 / 70 (44% complete)
**Commits:** ~62
**Deadline:** 20.12.2026
**Days remaining:** 58

## Что уже работает

- **17 команд** в боте
- **5 таблиц** в БД (users, habits, checkins, user_settings, reflections)
- **Утренний дайджест** с привычками, словом дня и печенькой
- **Вечерняя рефлексия** (FSM-диалог)
- **Инлайн-кнопки** в `/today`
- **Графики** через matplotlib
- **CSV-экспорт** для анализа в Excel
- **Docker** для деплоя
- **14 автотестов** + GitHub Actions
- **Интерактивное меню** с разделами
- **5 тем слов** — 151 слово

## Что осталось

- **Деплой на VPS** — чтобы бот работал 24/7
- **Тесты для новых фич** — `/export`, `/cookie`, streak
- **Полировка README** — блоки кода
- **GIF-демо** — для портфолио
- **Презентация** — для защиты проекта