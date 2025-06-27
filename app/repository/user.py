from typing import Any, Type
import logging

from app.components.decorators.unique import unique_error
from app.components.exceptions import UnautorizedException
from app.components.utils import get_password_hash
from app.models import User
from app.repository.base import BaseRepository, CreatingSchemaType
from app.schemas import BaseSchema


logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User]):

    def get_model_class(self) -> Type[User]:
        return User

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
        if "invite_token" in fields:
            fields.pop("invite_token")
        if "password" in fields:
            fields["hashed_password"] = get_password_hash(fields.pop("password"))
        return fields


    @unique_error(error_class=UnautorizedException)
    async def create(self, 
        obj_in: CreatingSchemaType | dict[str, Any], **extra_model_fields
    ):
        return await super().create(obj_in, **extra_model_fields)
