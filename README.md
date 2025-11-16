# Questions&Answers API (Django REST Framework + PostgreSQL + Docker)

## О проекте
* Минимальный сервис вопросов и ответов
* Модели:
    * Question: id, text, created_at
    * Answer: id, question(FK), user_id(UUID), text, created_at
## Требования:
    * Нельзя создавать ответ к несуществуюшему вопросу
    * Один пользователь может добавлять несколько ответов к одому вопросу
    * Удаление вопроса каскадно удаляет ответы

## Эндпоинты
    * GET /api/v1/questions/ - список вопросов
    * POST /api/v1/questions/ - создать вопрос
    * GET /api/v1/questions/{id}/ - детали вопроса
    * ELETE /api/v1/questions/{id}/ - удалить вопрос (каскадно удалит ответы)
    * POST /api/v1/questions/{id}/answers/ - добавить ответ к вопросу
    * GET /api/v1/answers/{id}/ - получить ответ
    * DELETE /api/v1/answers/{id}/ - удалить ответ

## Поведение user_id
    * Клиент не вводит user_id. Он берется из:
    * Заголовка X-User-ID(если есть, UUID), либо cookie uid (генерируется автоматически при первом ответе)
    * Ответы одного пользователя связываются по uid


## Быстрый старт в Docker (Compose)
1. Требования
    Docker и Docker Compose v2 (docker compose version)
2. Подготовка env для Docker
    оздайте фалй .env.compose в корне (рядом с docker-compose.yml) по примеру .env.compose.example.
3. Запуск
    Первый запуск (с чистым томом БД): docker compose down -v docker compose up --build
    Открыть API: http://localhost:8000/api/v1/questions/


## Локальный запуск без Docker (опционально)

1. Устновить зависимовти
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

2. Подготовка .env
    Создайте файл .env в корне по примеру .env.example

3. Запуск
    python manage.py migrate
    python manage.py runserver
    Открыть http://127.0.0.1:8000/api/v1/questions/