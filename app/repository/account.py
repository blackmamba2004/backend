from typing import Any, Type
from uuid import UUID
import logging

from sqlalchemy import select, and_

from app.components.decorators.unique import unique_error
from app.components.exceptions import ConflictException
from app.models import BrokerServiceAccount, UserPermission
from app.repository.base import BaseRepository, CreatingSchemaType


logger = logging.getLogger(__name__)


class AccountRepository(BaseRepository[BrokerServiceAccount]):

    def get_model_class(self) -> Type[BrokerServiceAccount]:
        return BrokerServiceAccount


    @unique_error(
        error_class=ConflictException, 
        message="Account for this service already exists"
    )
    async def create(self, 
        obj_in: CreatingSchemaType | dict[str, Any], **extra_model_fields
    ):
        return await super().create(obj_in, **extra_model_fields)
    

    async def get_client_accounts_to_services(self, client_id: UUID):
        """SELECT bsa.id, bsa.service_id 
        FROM broker_service_accounts bsa 
        JOIN user_permissions up 
        ON bsa.id = up.broker_account_id 
        WHERE up.user_id = $1::UUID
        AND up.can_trade = TRUE"""

        query = (
            select(
                BrokerServiceAccount.__table__.c.id,
                BrokerServiceAccount.__table__.c.service_id
            )
            .join(
                UserPermission, 
                BrokerServiceAccount.id == UserPermission.broker_account_id
            )
            .where(
                and_(
                    UserPermission.user_id == client_id,
                    UserPermission.can_trade == True
                )
            )
        )
        res = (await self._session.execute(query)).all()
        return res