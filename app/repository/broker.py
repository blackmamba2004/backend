from typing import Any, Type

from sqlalchemy import select, exists

from app.components.utils import get_password_hash
from app.models import Broker
from app.repository.base import BaseRepository
from app.schemas import BaseSchema


class BrokerRepository(BaseRepository[Broker]):

    def get_model_class(self) -> Type[Broker]:
        return Broker

    async def _adapt_fields(
        self, obj: dict[str, Any] | BaseSchema, **kwargs
    ) -> dict[str, Any]:
        fields = await super()._adapt_fields(obj, **kwargs)
        if "email" in fields:
            fields["email"] = (
                fields["email"].lower()
                if isinstance(fields["email"], str)
                else fields["email"]
            )
        if "password" in fields:
            fields["hashed_password"] = get_password_hash(fields.pop("password"))
        return fields
