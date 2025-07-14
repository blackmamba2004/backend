from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar, Sequence
from uuid import UUID

import logging

from sqlalchemy import (
    and_, or_, select, exists, inspect, Result, Executable, delete, insert
)
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.asyncio import AsyncSession

from app.components.exceptions import NotFoundException
from app.models import BaseModel
from app.schemas import BaseSchema

logger = logging.getLogger(__name__)


ModelType = TypeVar("ModelType", bound=BaseModel)
CreatingSchemaType = TypeVar("CreatingSchemaType", bound=BaseSchema)
UpdatingSchemaType = TypeVar("UpdatingSchemaType", bound=BaseSchema)


class NullColumn:
    """
    Класс для замены None при явной передаче значения null с API в DTO.
    Предназначен для адекватной передачи установки значений None при обновлении записей в репозитории SQLAlchemy.
    """
    pass


class BaseRepository(ABC, Generic[ModelType]):
    """
    Базовый класс репозитория, инкапсулирующий базовые методы для работы с базой данных через SQLAlchemy
    """

    _model_class: Type[ModelType]

    def __init__(self):
        self._model_class = self.get_model_class()

    def set_session(self, session: AsyncSession):
        self._session = session

    abstractmethod
    def get_model_class(self) -> Type[ModelType]:
        """
        Получить класс модели

        :return: Класс модели SQLAlchemy
        """
        raise NotImplementedError()

    async def find_by_id(self, id_: int | str | UUID, exception_on_none: bool = False) -> ModelType | None:
        """
        Найти модель в базе данных по её ID

        :param id_: ID модели
        :param exception_on_none: Нужно ли выбрасывать исключение, если объект не найден
        :return: Объект модели или None, если модель не найдена
        """
        instance = await self._session.get(self._model_class, id_)
        if exception_on_none and instance is None:
            raise NotFoundException(f"{self.get_model_class().__name__} with ID={id_} not found")

        return instance

    async def find_one(self, exception_on_none: bool = False, **filters) -> ModelType | None:
        """
        Найти модель в базе данных по фильтрам

        :param exception_on_none: Нужно ли выбрасывать исключение, если объект не найден
        :param filters: Фильтры, переданные в виде именованных аргументов
        :return: Объект модели или None, если модель не найдена
        """
        query = select(self._model_class).filter_by(**filters).limit(1)
        instance = (await self._get_query_result(query)).scalars().first()
        if exception_on_none and instance is None:
            raise NotFoundException(f"{self.get_model_class().__name__} with ID={id} not found")

        return instance

    async def find_all(self, **filters) -> Sequence[ModelType]:
        """
        Найти все модели в базе данных по фильтрам

        :param filters: Фильтры, переданные в виде именованных аргументов
        :return: Список объектов моделей
        """
        query = select(self._model_class).filter_by(**filters)
        return (await self._get_query_result(query)).scalars().all()
    
    async def delete_by_id(self, id: str | int | UUID) -> None:
        """
        Удалить запись из базы данных по её ID.

        :param id: UUID записи для удаления
        """
        if isinstance(id, UUID):
            id = str(id)
        stmt = delete(self._model_class).where(self._model_class.id == id)
        await self._get_query_result(stmt)
    
    async def delete_by_filters(self, **filters) -> None:
        """
        Удалить запись из базы данных по фильтрам.
        """
        stmt = delete(self._model_class).where(**filters)
        await self._get_query_result(stmt)
    
    async def _adapt_fields(
        self, obj: dict[str, Any] | BaseSchema, **kwargs
    ) -> dict[str, Any]:
        """
        Преобразовать поля в словарь
        :param obj: словарь или DTO
        :param kwargs: поименованные поля
        :return:
        """
        if isinstance(obj, dict):
            data = obj
        else:
            data = obj.model_dump(exclude_unset=True)
        data.update(**kwargs)
        return data

    async def _set_db_obj_fields(
        self, db_obj: ModelType, fields: dict[str, Any]
    ) -> ModelType:
        """
        задание аттрибутов модели
        :param db_obj: модель SQLAlchemy
        :param fields: устанавливаемые аттрибуты
        :return: объект с состоянием Transient
        """
        info = inspect(self._model_class)
        if info is None:
            raise ValueError(f"Inspection of {self._model_class} returned None.")

        for field in info.columns.keys() + info.relationships.keys():
            if field in fields:
                setattr(db_obj, field, fields[field])
        return db_obj

    async def create(
        self, obj_in: CreatingSchemaType | dict[str, Any], **kwargs
    ) -> ModelType:
        """
        Создать запись в БД
        :param obj_in: DTO или словарь
        :param kwargs: поименованные поля

        :return: объект с состоянием Pending
        """
        db_obj = self._model_class()
        fields = await self._adapt_fields(obj_in, **kwargs)
        db_obj = await self._set_db_obj_fields(db_obj=db_obj, fields=fields)
        self._session.add(db_obj)
        await self._session.flush()
        await self._session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdatingSchemaType | dict[str, Any],
        **kwargs,
    ) -> ModelType:
        fields = await self._adapt_fields(obj_in, **kwargs)
        db_obj = await self._set_db_obj_fields(db_obj=db_obj, fields=fields)
        self._session.add(db_obj)
        await self._session.flush()
        await self._session.refresh(db_obj)
        return db_obj

    async def _get_query_result(self, query: Executable) -> Result:
        """
        Получить результат запроса

        :param query: Executable запрос
        :result: Result - экземпляра ответа на запрос в базу данных
        """
        return await self._session.execute(query)
    
    async def exists_by_field(self, **filters) -> bool:
        """
        Существует ли модель по фильтрам
        """
        conditions = [
            getattr(self._model_class, key) == value
            for key, value in filters.items()
        ]

        query = (
            select(
               exists().where(and_(*conditions))
            ).limit(1)
        )

        return (await self._session.execute(query)).scalar()
    
    async def exists_by_any_field(self, **filters) -> bool:
        """
        Существует ли модель хотя бы по одному фильтру
        """
        conditions = [
            getattr(self._model_class, key) == value
            for key, value in filters.items()
        ]

        query = (
            select(
               exists().where(or_(*conditions))
            ).limit(1)
        )

        return (await self._session.execute(query)).scalar()
    
    async def _convert_model_to_dict(self, model: BaseModel) -> dict:
        """
        Преобразовать значения из модели в словарь.
        Убрать все None значения, значения NullColumn заменить на None.

        :param model: Модель для преобразования
        :return: Словарь для использования в SQLAlchemy
        """
        self.validate_model(model)
        columns = model.__table__.columns.keys()
        result_dict = {}
        for column in columns:
            attr = getattr(model, column)
            if isinstance(attr, NullColumn):
                result_dict[column] = None
            elif attr is not None:
                result_dict[column] = attr

        return result_dict

    def validate_model(self, model: ModelType | Mapped[ModelType]) -> None:
        """
        Выполнить базовую валидацию модели перед сохранением.

        :param model: Модель для валидации
        """
        if not isinstance(model, self._model_class):
            raise ValueError(f"Invalid model type: expected {self._model_class.__name__}, got {type(model).__name__}")
        
    async def bulk_insert(self, models: Sequence[ModelType]) -> None:
        """
        Массовая вставка записей в базу данных.

        :param models: Список моделей для вставки
        """
        values = [await self._convert_model_to_dict(model) for model in models]
        stmt = insert(self._model_class).values(values)
        await self._session.execute(stmt)