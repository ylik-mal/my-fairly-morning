# Roadmap — My Fairly Morning 🌅

План развития проекта на 10 недель.

## ✅ Week 1 — Foundation
- [x] Project structure and Git setup
- [x] aiogram 3 + bot initialization
- [x] `/start` command handler
- [x] SOCKS5 proxy support for restricted regions

## 🚧 Week 2 — Database
- [ ] SQLite connection module
- [ ] `users` and `habits` tables
- [ ] `/add_habit` command
- [ ] `/my_habits` command
- [ ] `/delete_habit` command

## 📅 Week 3 — Daily check-ins
- [ ] `checkins` table
- [ ] Inline buttons: Done / Skipped
- [ ] `/today` — today's habits list

## 📅 Week 4 — Morning digest
- [ ] APScheduler integration
- [ ] `/set_morning` — choose time
- [ ] Auto-send morning habits list

## 📅 Week 5 — Evening reflection
- [ ] `/set_evening` — choose time
- [ ] FSM dialogue for reflection
- [ ] Save reflections to database

## 📅 Week 6 — Text statistics
- [ ] `/stats` — weekly summary
- [ ] Streak calculation
- [ ] Completion percentage

## 📅 Week 7 — Visualization
- [ ] matplotlib charts
- [ ] `/chart` — send chart as image
- [ ] 7-day and 30-day views

## 📅 Week 8 — UX improvements
- [ ] Onboarding FSM for new users
- [ ] Default habit set
- [ ] Settings: timezone, name
- [ ] Emoji and inline keyboards polish

## 📅 Week 9 — Code quality
- [ ] Error handling and logging
- [ ] pytest tests
- [ ] Docstrings
- [ ] Refactoring

## 📅 Week 10 — Release
- [ ] Deploy to VPS (24/7)
- [ ] GitHub Actions CI
- [ ] README with demo GIF
- [ ] Final presentation