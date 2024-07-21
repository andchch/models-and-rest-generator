# CLI приложения для генерации Pydantic моделей и REST API контроллеров

## Реализованные возможности

**CLI** приложение:
- Генерация Pydantic моделей на основе JSON схем
- Генерация контроллеров FastAPI на основе добавленных Pydantic моделей
- Управление миграциями Alembic


**API** приложение позволяет:
- **Получать** JSON документы из базы данных
- **Добавлять** JSON документы в базу данных
- **Изменять** JSON документы в базе данных
- **Удалять** JSON документы из базы данных
- Отправлять вообщения в Kafka брокер после выполнения POST, PUT и DELETE запросов
- **Автоматическое обновление** Swagger документации API после изменения/добавления/удаления файлов

## Установка

1. Клонировать репозиторий и перейти в деиректорию

    ```bash
    git clone https://github.com/andchch/models-and-rest-generator.git
    cd models-and-rest-generator
    ```

2. Настроить виртуальное окружение в зависимости от ОС

    ```bash
   MacOS/Linux:

    python -m venv .venv
    source .venv/bin/activate
    ```
   ```bash
    Windows:
   python -m venv .venv
   .venv\Scripts\Activate.ps1
    ```
3. Установить зависимости

   ```bash
    pip install -r requirements/prod-requirements.txt
    ```

## Использование
JSON схемы должны соответвовать стандарту JSON Schema Draft 7 и обязательно иметь свойства kind, version, description, name, configuration.

**Свойство kind должно иметь свойтво `default` с названием kind модели.**
### CLI приложение
- Помощь по командам
```bash
python cli/cli.py --help
```
- Генерация Pydantic моделей на основе JSON схемы
```bash
python cli/cli.py gen-models --json-schema=<путь к JSON схеме>
```
Сгенерированные модели будут сохранены в папке `api/models`
- Генерация контроллеров FastAPI на основе добавленных Pydantic моделей
```bash
python cli/cli.py gen-controllers
```
Команда создаст контроллеры для всех моделей, которые находятся в папке `api/models`

Сгенерированные контроллеры будут сохранены в папке `api/routes`
- Управление миграциями Alembic
```bash
alembic --help
Все доступные команды Alembic
```
### REST API приложение
#### Предварительные настройки
- Перед началом работы необходимо создать файл `.env` в корне проекта и заполнить его данными:
Пример файла `.env`:
```text
DATABASE_URL=
KAFKA=
```
Где `DATABASE_URL` - строка подключения SQLAlchemy к базе данных PostgreSQL

`KAFKA` - строка подключения к брокеру сообщений Kafka

Значения по умолчанию:
```text
DATABASE_URL=postgresql+asyncpg://postgres:example@localhost:5432/postgres
KAFKA=localhost:9092
```
**! Драйвер для работы с PostgreSQL - `asyncpg` !**
- Дополнительно перед началом работы необходимо применить миграции к базе данных:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
````
- Запуск API
```bash
С активированным виртуальным окружением:
python api/main.py
```

После запуска приложения, Swagger документация будет доступна по адресу `http://localhost:8000/docs`

## Пример использования
- Исходная схема находится в файле `test/test_schema.json`
- Модель сгенерирована в файле `api/models/vk_test.py`
- Контроллеры сгенерированы в файле `api/routes/vk_test.py`


### Flowchart CLI
![Flowchart ClI](docs/readme/cli.png)
### Flowchart диаграмма REST API приложения
![Flowchart REST API](docs/readme/rest.png)
### Таблица в базе данных
![DB](docs/readme/db_ERD.png)