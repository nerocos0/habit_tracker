# Habit Tracker

Веб-приложение для отслеживания привычек с REST API, JWT-аутентификацией и автоматическим CI/CD.

## Live Demo

- Сайт: https://habitracker.duckdns.org/
- API документация (Swagger): https://habitracker.duckdns.org/api/docs/

## Возможности

- Регистрация и аутентификация через JWT
- Создание, редактирование и удаление привычек
- Отметка выполнения привычек по дням
- Пауза и возобновление привычек
- Целевое количество выполнений в день
- Фильтрация, поиск и сортировка привычек
- Пагинация результатов
- Автоматический подсчёт выполненных дней
- Разграничение прав доступа (только владелец может изменять)
- REST API с документацией Swagger
- Покрытие тестами (30+ тестов)
- Docker-контейнеризация
- CI/CD через GitHub Actions

## Стек технологий

Backend:
- Python 3.13
- Django 6.1
- Django REST Framework
- PostgreSQL 16
- JWT (djangorestframework-simplejwt)
- drf-spectacular (OpenAPI / Swagger)
- django-filter

Frontend:
- Django Templates
- HTML / CSS

Инфраструктура:
- Docker / Docker Compose
- Nginx (reverse proxy)
- Gunicorn (WSGI)
- Let's Encrypt (HTTPS)
- Certbot (автообновление сертификатов)

CI/CD:
- GitHub Actions
- GitHub Container Registry (GHCR)

Хостинг:
- VPS (Ubuntu)

## Локальный запуск

Требования:
- Python 3.13+
- PostgreSQL 16+
- Git

Шаги:

1. Клонировать репозиторий:
   ```bash
   git clone git@github.com:nerocos0/habit_tracker.git
   cd habit_tracker
   ```

2. Создать виртуальное окружение:
   ```bash
   python -m venv venv

   # Linux / macOS
   source venv/bin/activate

   # Windows (PowerShell)
   venv\Scripts\activate
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создать базу данных PostgreSQL:
   ```sql
   CREATE DATABASE habit_tracker;
   CREATE USER habit WITH PASSWORD 'habit';
   ALTER ROLE habit CREATEDB;
   GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit;
   ```

   Команда ALTER ROLE habit CREATEDB нужна для запуска тестов — Django создаёт временную тестовую БД.

5. Создать файл .env в корне проекта:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   POSTGRES_DB=habit_tracker
   POSTGRES_USER=habit
   POSTGRES_PASSWORD=habit
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

   SECRET_KEY можно сгенерировать:
   ```bash
   python -c "from django.core.management.utils import get_random_string; print(get_random_string(64))"
   ```

6. Применить миграции:
   ```bash
   python manage.py migrate
   ```

7. Создать суперпользователя (опционально):
   ```bash
   python manage.py createsuperuser
   ```

8. Запустить сервер разработки:
   ```bash
   python manage.py runserver
   ```

зайти на локалхост

## Тесты

```bash
python manage.py test
```

Покрытие: модели, аутентификация, views, API endpoints.

## CI/CD

Проект настроен на автоматический CI/CD через GitHub Actions:

- CI — при каждом push в master запускаются тесты
- CD — после успешного CI:
  1. Собирается Docker-образ
  2. Образ пушится в GitHub Container Registry (GHCR)
  3. Образ автоматически деплоится на сервер по SSH

## Безопасность

- HTTPS через Let's Encrypt
- HSTS включён
- Secure cookies (SESSION, CSRF)
- DEBUG=False на проде
- Секреты в .env (не в git)
- JWT с ограниченным временем жизни
- deployer-пользователь без root-прав для CD
- Deploy Key (read-only) для git pull на сервере
- Fail2ban для защиты SSH

## Автор

Nerocos0
GitHub: https://github.com/nerocos0


Это учебный проект.