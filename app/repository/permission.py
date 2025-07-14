from typing import Any, Type
from uuid import UUID
import logging

from sqlalchemy import select, and_

from app.components.decorators.unique import unique_error
from app.components.exceptions import ConflictException
from app.models import UserPermission, BrokerServiceAccount
from app.repository.base import BaseRepository, CreatingSchemaType


logger = logging.getLogger(__name__)


class UserPermissionRepository(BaseRepository[UserPermission]):

    def get_model_class(self) -> Type[UserPermission]:
        return UserPermission
    
    @unique_error(
        error_class=ConflictException, 
        message="Permissions for this user already exist"
    )
    async def create(self, 
        obj_in: CreatingSchemaType | dict[str, Any], **extra_model_fields
    ):
        return await super().create(obj_in, **extra_model_fields)

    async def has_permissions(self, broker_account_id: UUID, user_id: UUID):
        query = (
            select(UserPermission.__table__.c.can_trade)
            .where(
                and_(
                    UserPermission.broker_account_id == broker_account_id,
                    UserPermission.user_id == user_id
                )
            )
        )

        return (await self._session.execute(query)).scalar()
    

    async def select_many_account_data(self):
        """SELECT bsa.login, bsa.password 
        FROM broker_service_accounts bsa 
        JOIN user_permissions up 
        ON bsa.id = up.broker_account_id 
        WHERE up.user_id = 'ef21ecfd-dec4-4a70-9f51-817986a4c3d9' 
        AND up.can_trade = TRUE"""

        pass
