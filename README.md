# Сервис расчёта стоимости страхования

Этот сервис предоставляет REST API для расчёта стоимости страхования на основе типа груза и объявленной стоимости (ОС).

## Используемые технологии

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Docker
- Docker-compose

## Начало работы

### Предварительные требования

- Docker
- Docker-compose

### Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone <repository_url>
   cd insurance_service
   ```

2. Запустите сервис с помощью Docker Compose:

   ```bash
   docker-compose up --build
   ```
