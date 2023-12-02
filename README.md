# Marketplace
Сервис по размещению объявлений. Объявления могут быть разных видов (продажа, покупка, оказание услуг).
Основные роли системы: пользователь, администратор.

## Описание стека технологий
- Платформа - WSL2 Ubuntu 20.04.2
- Яп - Python 3.10
- Менеджер зависимостей - Poetry 1.6.1
- Docker Engine 24.0.6, Docker 20.10.7, Docker Compose 2.21.0
- Линтинг - wemake-python-styleguide 0.18.0
- База данных - PostgreSQL 16.1

## Документация OpenAPI (Swagger)
Файл с документацией: `openapi.json`

## Развертывание и остановка сервиса
### С помощью docker-compose
```sh
docker-compose up -d
docker-compose down
```
### Без использования docker-compose и Dockerfile
```sh
poetry install
docker run -d -e POSTGRES_PASSWORD='admin' -e POSTGRES_USER='admin' -e POSTGRES_DB='marketplace' -p 5432:5432 --name=postgres-test postgres
poetry run alembic upgrade head
poetry run python src/app/service.py
```

##  Конфигурация проекта
### Конфигурация проекта с помощью изменения файла конфигурации
Файл с конфигурацией: `src/config/config.yml`

Конфигурация FastAPI приложения
```
service:
  host: '0.0.0.0'
  port: 8080
```

Конфигурация токена доступа (jwt)
```
access_token:
  token_type: 'bearer'
  expire_days: 7 
  secret: 'super_secret_secret'
```

Конфигурация параметров соединения с postgres
```
postgres:
  login: 'admin'
  password: 'admin'
  db_name: 'marketplace'
  host: '0.0.0.0'
  port: 5432
```

### Конфигурация проекта с помощью docker-compose и переменных окружения
Чтобы изменить параметр конфигурации указанной выше можно использовать переменные окружения с приставкой `EMP_`.
Например, чтобы изменить порт на котором запускается сервис (без докера): `export EMP_SERVICE='{"port": 24123}'`.

Также параметр можно изменить в файле `docker-compose.yml`, в блоке environment:
```
environment:
  - EMP_SERVICE={"port":24123}
```
