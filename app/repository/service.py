from typing import Any, Type
import logging

from app.components.decorators.unique import unique_error
from app.components.exceptions import ConflictException
from app.models import Service
from app.repository.base import BaseRepository, CreatingSchemaType


logger = logging.getLogger(__name__)


class ServiceRepository(BaseRepository[Service]):

    def get_model_class(self) -> Type[Service]:
        return Service

    @unique_error(error_class=ConflictException, message="This service's name already exists")
    async def create(self, obj_in: CreatingSchemaType | dict[str, Any], **extra_model_fields):
        return await super().create(obj_in, **extra_model_fields)
    

    @unique_error(error_class=ConflictException, message="This service's name already exists")
    async def update(
        self, db_obj: Service, obj_in: CreatingSchemaType | dict[str, Any], **extra_model_fields
    ):
        return await super().update(db_obj=db_obj, obj_in=obj_in, **extra_model_fields)
