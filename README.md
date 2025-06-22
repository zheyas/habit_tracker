# Habit Tracker API

## Описание

REST API для приложения "Трекер Привычек", разработанного с использованием Django REST Framework. Это API предоставляет возможность пользователям регистрироваться, аутентифицироваться, создавать, редактировать и просматривать свои привычки, а также просматривать публичные привычки других пользователей. Также реализована интеграция с Telegram для отправки уведомлений.

## Технологии

*   **Python:** 3.10 или выше
*   **Django:** 4.2 или выше
*   **Django REST Framework:** Для создания RESTful API
*   **PostgreSQL:** В качестве базы данных
*   **django-rest-framework-simplejwt:** Для JWT аутентификации
*   **python-telegram-bot[job-queue]:** Для взаимодействия с Telegram Bot API
*   **Celery:** Для асинхронных задач (отправка уведомлений в Telegram)
*   **Redis:** В качестве брокера сообщений для Celery
*   **django-celery-beat:** Для планирования задач Celery
*   **python-dotenv:** Для управления переменными окружения

## Установка

1.  **Клонируйте репозиторий:**

    ```bash
    git clone <repository_url>
    cd habit_tracker
    ```

2.  **Создайте виртуальное окружение:**

    ```bash
    python -m venv venv
    ```

3.  **Активируйте виртуальное окружение:**

    *   **Linux/macOS:**

        ```bash
        source venv/bin/activate
        ```

    *   **Windows:**

        ```bash
        venv\Scripts\activate
        ```

4.  **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

    (Если у вас нет файла `requirements.txt`, создайте его и добавьте туда все необходимые пакеты. Пример содержимого `requirements.txt`:)

    ```
    Django>=4.2
    djangorestframework
    djangorestframework-simplejwt
    psycopg2-binary
    python-dotenv
    django-cors-headers
    celery
    redis
    django-celery-beat
    python-telegram-bot[job-queue]
    ```

5.  **Настройте PostgreSQL:**

    *   Установите PostgreSQL, если он еще не установлен.
    *   Создайте пользователя и базу данных для вашего проекта.
    *   Предоставьте пользователю права на базу данных.

6.  **Настройте переменные окружения:**

    *   Создайте файл `.env` в корневой директории проекта.
    *   Добавьте следующие переменные окружения:

        ```
        DJANGO_SECRET_KEY=<your_secret_key>
        DJANGO_DEBUG=True
        DATABASE_URL=postgres://<your_user>:<your_password>@<your_host>:<your_port>/<your_database>
        TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
        ```

        Замените `<your_secret_key>`, `<your_user>`, `<your_password>`, `<your_host>`, `<your_port>`, `<your_database>` и `<your_telegram_bot_token>` на соответствующие значения.
        *   **`DJANGO_SECRET_KEY`:** Сгенерируйте сложный и случайный секретный ключ.
        *   **`DATABASE_URL`:** URL для подключения к базе данных PostgreSQL.
        *   **`TELEGRAM_BOT_TOKEN`:** Токен вашего Telegram-бота, полученный от BotFather.

7.  **Примените миграции:**

    ```bash
    python manage.py makemigrations users
    python manage.py makemigrations habits
    python manage.py migrate
    ```

8.  **Создайте суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```

9.  **Запустите сервер Django:**

    ```bash
    python manage.py runserver
    ```

10. **Запустите Celery worker и Celery beat:**

    *   В отдельных терминалах:

        ```bash
        celery -A config worker -l INFO
        celery -A config beat -l INFO
        ```

## API Эндпоинты

### Аутентификация

*   **`POST /api/users/register/`:** Регистрация нового пользователя.
    *   **Параметры:** `username`, `email`, `password`
*   **`POST /api/users/login/`:** Авторизация пользователя.
    *   **Параметры:** `email`, `password`
    *   **Возвращает:** JWT access и refresh токены.
*   **`POST /api/users/token/`:** Получение JWT access и refresh токенов.
    *   **Параметры:** `email`, `password`
*   **`POST /api/users/token/refresh/`:** Обновление JWT access токена.
    *   **Параметры:** `refresh`
    *   **Заголовок `Authorization`:** Не требуется

### Привычки

*   **`GET /api/habits/`:** Получение списка привычек текущего пользователя (требуется аутентификация).
    *   **Заголовок `Authorization`:** `Bearer <JWT_TOKEN>`
    *   **Пагинация:** Используется пагинация с 5 привычками на странице.
*   **`POST /api/habits/`:** Создание новой привычки (требуется аутентификация).
    *   **Заголовок `Authorization`:** `Bearer <JWT_TOKEN>`
    *   **Параметры:** `place`, `time`, `action`, `is_pleasant`, `related_habit` (опционально), `periodicity`, `reward` (опционально), `execution_time`, `is_public`
*   **`GET /api/habits/{id}/`:** Получение информации о конкретной привычке (требуется аутентификация).
    *   **Заголовок `Authorization`:** `Bearer <JWT_TOKEN>`
*   **`PUT /api/habits/{id}/`:** Обновление информации о привычке (требуется аутентификация).
    *   **Заголовок `Authorization`:** `Bearer <JWT_TOKEN>`
    *   **Параметры:** `place`, `time`, `action`, `is_pleasant`, `related_habit` (опционально), `periodicity`, `reward` (опционально), `execution_time`, `is_public`
*   **`DELETE /api/habits/{id}/`:** Удаление привычки (требуется аутентификация).
    *   **Заголовок `Authorization`:** `Bearer <JWT_TOKEN>`
*   **`GET /api/habits/public/`:** Получение списка публичных привычек (требуется аутентификация).
    *   **Заголовок `Authorization`:** `Bearer <JWT_TOKEN>`
    *   **Пагинация:** Используется пагинация с 5 привычками на странице.

## Интеграция с Telegram

При создании новой привычки пользователь получает уведомление в Telegram.  Для этого необходимо:

1.  Создать Telegram-бота и получить токен от BotFather.
2.  Указать токен в переменной окружения `TELEGRAM_BOT_TOKEN`.
3.  Получить `chat_id` пользователя и сохранить его в поле `telegram_chat_id` модели User.
4.  Запустить Celery worker и Celery beat для обработки асинхронных задач.

## Дополнительная информация

*   Для доступа к админ-панели Django перейдите по адресу `/admin/` и войдите в систему с учетными данными суперпользователя.
