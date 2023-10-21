# Файл с основными настройками БД (подключение, создание сессий)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DATABASE_URL = settings.database_url


# создание асинхронного движка
engine = create_async_engine(DATABASE_URL)

# генератор для создания сессий (обработки транзакций)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# класс для акумуляции метаданных о всех таблицах (моделях)
# используется для миграций
class Base(DeclarativeBase):
    pass