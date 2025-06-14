from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession

from app.repository.base import BaseRepository
from app.unit_of_work.abstract import AbstractUnitOfWork
from app.components.utils import camel_to_snake


class BaseUnitOfWork(AbstractUnitOfWork):
    """
    Реализация паттерна UnitOfWork для SQLAlchemy.
    Использует неявную установку объектов репозиториев в поля класса.
    """

    def __init__(
            self,
            session: AsyncSession,
            repository_list: list[BaseRepository],
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.session = session
        self.repository_list = repository_list
        self._init_repository_properties(repository_list)
    
    def _init_repository_properties(self, repository_list: list[BaseRepository]) -> None:
        """
        Инициализировать переданные репозитории, как поля класса
        :param repository_list:
        :return:
        """
        for repository in repository_list:
            attribute_name = camel_to_snake(repository.__class__.__name__)
            if not hasattr(self, attribute_name):
                raise AttributeError(f"Attribute {attribute_name} not found in UOW {self.__name__}.")
            setattr(self, attribute_name, repository)

    async def __aenter__(self):
        await self._set_session_in_repositories()
        return self

    async def _set_session_in_repositories(self):
        """
        Установить сессию в репозитории
        :return:
        """
        for repository in self.repository_list:
            repository.set_session(self.session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        """
        Откатить изменения сессии
        :return:
        """
        await self.session.rollback()

    async def flush(self) -> None:
        """
        Обновление всех объектов в сессии в соответствии с базой данных (например, установка ID в новые записи)
        :return:
        """
        await self.session.flush()

    async def refresh(self, instance) -> None:
        """
        Обновить значения в объекте в соответствии с базой данных
        :param instance:
        :return:
        """
        await self.session.refresh(instance)

    async def begin_nested(self) -> AsyncSessionTransaction:
        """
        Начать внутреннюю транзакцию
        :return:
        """
        return self.session.begin_nested()

    async def close(self):
        return await self.session.close()
