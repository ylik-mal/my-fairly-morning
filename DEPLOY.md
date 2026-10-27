# DEPLOY — развёртывание на VPS

Пошаговая инструкция для развёртывания бота на VPS с Docker.

## 1. Подготовка VPS

### Требования
- VPS с Ubuntu 22.04+ (или Debian 11+)
- 1 vCPU, 1 ГБ RAM, 10 ГБ диска
- Доступ по SSH (root или пользователь с sudo)

### Подключение
```bash
ssh root@IP_АДРЕС_ВАШЕГО_VPS
2. Установка Docker
bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Проверка
docker --version
docker compose version
3. Клонирование проекта
bash
cd /opt
git clone https://github.com/ylik-mal/my-fairly-morning.git
cd my-fairly-morning
4. Настройка .env
bash
cp .env.example .env
nano .env
Заполнить:

text
BOT_TOKEN=ваш_токен_от_BotFather
PROXY=socks5://IP:PORT
Важно: если VPS за пределами РФ — PROXY можно оставить пустым.

5. Запуск
bash
docker compose up -d
Проверка логов:

bash
docker compose logs -f
Должно быть: INFO - Бот запущен.

6. Управление
Команда	Действие
docker compose logs -f	Логи в реальном времени
docker compose restart	Перезапуск
docker compose down	Остановка
docker compose up -d	Запуск
docker compose up -d --build	Пересборка после изменений
7. Автозапуск при перезагрузке
Создать systemd-сервис:

bash
sudo nano /etc/systemd/system/my-fairly-morning.service
Вставить:

ini
[Unit]
Description=My Fairly Morning Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/opt/my-fairly-morning
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
ExecReload=/usr/bin/docker compose restart

[Install]
WantedBy=multi-user.target
Активировать:

bash
sudo systemctl daemon-reload
sudo systemctl enable --now my-fairly-morning
8. Проверка
bash
sudo systemctl status my-fairly-morning
docker compose ps
Бот должен быть Up.

9. Обновление бота
bash
cd /opt/my-fairly-morning
git pull
docker compose up -d --build
Troubleshooting
Бот не подключается к Telegram
Проверь PROXY в .env (если VPS в РФ — нужен прокси).

Логи: docker compose logs -f.

Ошибка Cannot connect to host api.telegram.org
VPS в РФ без прокси → добавь PROXY в .env.

Docker Compose не запускается
Проверь: docker compose config.

Проверь .env — все переменные заполнены.

Безопасность
✅ .env не коммитится в Git (в .gitignore).

✅ VPS с firewall (ufw) — открыты только нужные порты.

✅ Регулярное обновление: sudo apt update && sudo apt upgrade.

Источники
Docker: установка на Ubuntu

Docker Compose: документация

Systemd: автозапуск сервисов