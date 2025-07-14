import logging
from uuid import UUID

from app.models import User

from app.schemas.dto import ChangeUserPermissionsDTO
from app.schemas.responses import Response
from app.unit_of_work import UserUnitOfWork


logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self, unit_of_work: UserUnitOfWork,
    ):
        self._uow = unit_of_work

    async def get_my_clients(self, broker: User):
        async with self._uow as uow:
            return await uow.user_repository.get_clients_with_permissions(broker.id)

    async def change_user_permissions(
        self, broker_id: UUID, account_id: UUID, client_id: UUID, 
        data: ChangeUserPermissionsDTO
    ):
        async with self._uow as uow:
            await uow.user_repository.update_client_permissions(
                broker_id, account_id, client_id, data
            )
            await uow.commit()
        
        return Response(message="User permissions changed")