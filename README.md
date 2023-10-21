
# Описание проекта

Тестовое задание для Bewise.



# Ссылки
## FastAPI
1. http://127.0.0.1:8000
2. http://127.0.0.1:8000/docs

## pgAdmin4
1. http://localhost:5050/



# Запуск 

## Запуск виртуального окружения poetry
```bash
    poetry shell
```
## Запуск docker-compose (PostgreSQL и pgAdmin4)
```bash
    sudo docker-compose -f docker-compose.yaml up -d
```

## Запуск uvicorn
```bash
    uvicorn app.main:app --reload
```

# Отключение

## Отключить docker-compose
```bash
    docker-compose stop
```


# Файлы

* .env --- файл с чувствительными данными
* config.py --- хранит данных для подключений





# БД


## Добавление данных в БД
1. При создании моделий нужно добавить их импорты в папку app/migrations/env.py

```bash
alembic revision --autogenerate -m "Comment_1"
```

## Откат БД

### Вариант 1
* Для отката используется downgrade, после в app\migrations\versions удаляется сгенерированный ранее файл миграции


