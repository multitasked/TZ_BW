# Репозиторий или DAO отвечают за 
# отделение слоя работы с базой данных от бизнес-логики.


from app.database import async_session_maker
from sqlalchemy import insert, select, delete


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        ''' Найти элемент по id '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        ''' Найти один элемент по фильтрам '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def find_all(cls, **filter_by):
        ''' Найти все элементы по фильтрам '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by) # запрос в БД
            result = await session.execute(query)
            result = result.scalars().all() # .scalars().all() можно использовать только один раз
            return result # FastAPI сам сконвертирует результат в JSON


    @classmethod
    async def add(cls, **data):
        ''' Добавить элемент в таблицу '''
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)    # .returning() --- insert вывод заданный результат
            await session.execute(query)                # .execute(query) --- выполнить запрос
            await session.commit()                      # .commit() --- позволяет зафиксировать изменения в БД

    
    @classmethod
    async def delete(cls, **data):
        ''' Удалить элемент из таблицы '''
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**data).returning(cls.model)
            del_item = await session.execute(query)    
            await session.commit()            
            del_item = del_item.scalars().all()           
            return del_item


