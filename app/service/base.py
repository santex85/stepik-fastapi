# Импортируем необходимые библиотеки и инструменты
from app.database import async_session_maker
from sqlalchemy import select, insert


# Определение базового класса для работы с базой данных
class BaseService:
    """
    Базовый класс службы для работы с моделями SQLAlchemy.

    Этот класс предоставляет методы для основных CRUD-операций (создание, чтение, обновление, удаление)
    с использованием асинхронного программирования.
    """

    # Атрибут модели, который должен быть переопределен в подклассах
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        """
        Асинхронный метод для поиска записи по ID.

        Args:
            model_id (int): ID записи для поиска.

        Returns:
            dict: Найденная запись или None, если запись не найдена.
        """
        # Создаем асинхронную сессию с базой данных
        async with async_session_maker() as session:
            # Формируем запрос на выборку по ID
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            # Выполняем запрос
            result = await session.execute(query)
            # Возвращаем результат или None
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Асинхронный метод для поиска одной записи по заданным фильтрам.

        Args:
            **filter_by: Параметры фильтрации.

        Returns:
            dict: Найденная запись или None, если запись не найдена.
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Асинхронный метод для поиска всех записей по заданным фильтрам.

        Args:
            **filter_by: Параметры фильтрации.

        Returns:
            list[dict]: Список найденных записей.
        """
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model.__table__.columns).values(**data)
            await session.execute(query)
            await session.commit()
