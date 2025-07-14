from typing import Any, Sequence, Type, Tuple
from uuid import UUID
import logging

from sqlalchemy import select, update, and_, Row

from app.components.decorators.unique import unique_error
from app.components.exceptions import UnautorizedException
from app.components.utils import get_password_hash
from app.models import User, UserPermission
from app.models.user import UserRole
from app.repository.base import BaseRepository, CreatingSchemaType
from app.schemas import BaseSchema
from app.schemas.dto import ChangeUserPermissionsDTO


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

    @unique_error(error_class=UnautorizedException, message="User with this email or phone already exists")
    async def create(self, 
        obj_in: CreatingSchemaType | dict[str, Any], **extra_model_fields
    ):
        return await super().create(obj_in, **extra_model_fields)

    async def get_clients_with_permissions(self, broker_id):
        query = (
            select(
                User.__table__.c.id, 
                User.__table__.c.first_name,
                User.__table__.c.last_name,
                User.__table__.c.email, 
                User.__table__.c.tel, 
                User.__table__.c.is_active,
                User.__table__.c.created_at, 
                
                UserPermission.__table__.c.broker_account_id,
                UserPermission.__table__.c.can_trade,
            )
            .join(UserPermission, User.id == UserPermission.user_id)
            .where(
                and_(
                    User.ref_id == broker_id,
                    User.role == UserRole.USER
                )
            )
        )

        rows = (await self._session.execute(query)).all()

        return await self.serialize_users_with_permissions(rows)

    async def serialize_users_with_permissions(self, rows: Sequence[Row[Tuple]]):
        users_dict = {}

        for row in rows:
            (
                user_id, last_name, first_name, email, tel, 
                is_active, created_at, broker_account_id, can_trade
            ) = row

            if user_id not in users_dict:
                users_dict[user_id] = {
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "tel": tel,
                    "is_active": is_active,
                    "created_at": created_at,
                    "permissions": []
                }

            users_dict[user_id]["permissions"].append({
                "broker_account_id": broker_account_id,
                "can_trade": can_trade
            })

        return list(users_dict.values())

    async def update_client_permissions(
        self, 
        broker_id: UUID, 
        account_id: UUID, 
        client_id: UUID, 
        data: ChangeUserPermissionsDTO
    ) -> None:
        """
        UPDATE user_permissions up 
        SET can_trade = TRUE
        FROM users u
        WHERE up.user_id = u.id
        AND u.ref_id = '179dd004-d384-45b0-b795-16190325af1d'
        AND up.user_id = 'fdf7d3ba-abd2-4cc9-9265-2a5edcd6a9e8'
        AND up.broker_account_id = '3ff80062-f5bc-46db-8335-58df0b4276a0';
        """

        query = (
            update(UserPermission)
            .values(can_trade=data.can_trade)
            .where(
                and_(
                    UserPermission.user_id == User.id,
                    UserPermission.user_id == client_id,
                    UserPermission.broker_account_id == account_id,
                    User.ref_id == broker_id
                )
            )
        )
        await self._session.execute(query)