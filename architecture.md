# Архитектура проекта EDD Academy Bot

## Компоненты

1. Telegram Bot (`bot/`)
   - `aiogram`
   - обработка команд
   - меню и навигация
   - форма записи на курс
   - вызов API backend для получения данных

2. Backend API (`backend/`)
   - `Django + DRF`
   - бизнес-данные: курсы, новости, заявки, FAQ, контакты
   - REST API для бота и возможной веб-админки
   - админ-панель Django

3. PostgreSQL
   - хранение основной информации
   - модели: Course, News, Application, FAQ, About, etc.

4. Redis
   - кеширование списка новостей и курсов
   - брокер задач для Celery

5. Celery
   - фоновые задачи
   - загрузка/парсинг новостей из Telegram-канала
   - отправка уведомлений администратору

## Принципы
- Clean Architecture
- SOLID
- разделение по доменам:
  - `handlers` — Telegram
  - `services` — логика
  - `repositories` — работа с БД / API

## Базовая архитектура данных
- `Course`
- `NewsPost`
- `Application`
- `FAQ`
- `About`
- `Student`
- `Graduate`

## Поток данных

1. Пользователь открывает Telegram-бота
2. Бот запрашивает у backend актуальные курсы/новости
3. Пользователь отправляет заявку на курс
4. Заявка сохраняется в PostgreSQL
5. Celery уведомляет администратора

## Структура папок

```
EDD Academy Bot_ver-2/
├── backend/
│   ├── manage.py
│   ├── eddacademy/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── __init__.py
│   ├── apps/
│   │   ├── courses/
│   │   ├── news/
│   │   ├── applications/
│   │   ├── faq/
│   │   └── users/
│   └── requirements.txt
├── bot/
│   ├── app.py
│   ├── config.py
│   ├── handlers/
│   ├── services/
│   ├── repositories/
│   ├── keyboards/
│   └── schemas/
├── docker-compose.yml
└── .env.example
```

## Что делать первым
- реализовать минимальный MVP:
  - публичные курсы
  - публичные новости
  - запись на курс
  - базовое меню бота

## Далее
- студенческий авторизованный доступ
- выпускники и сертификаты
- интеграция с Google Calendar
- мультиязычность RU / EN / UZ
