import base64
import json
import logging

from uuid import UUID

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

from app.components import RedisCache
from app.models import User
from app.models.user import UserRole
from app.schemas.dto import (
    CreateAccountDTO, 
    UpdateAccountDTO
)
from app.schemas.responses import GetEncryptedAccountData, Response
from app.components.exceptions import ForbiddenException
from app.unit_of_work import AccountUnitOfWork


logger = logging.getLogger(__name__)


class AccountService:
    def __init__(
        self, 
        unit_of_work: AccountUnitOfWork,
        redis_cache: RedisCache
    ):
        self._uow = unit_of_work
        self._redis_cache = redis_cache

    async def create_account(self, body: CreateAccountDTO, **extra_model_fields):
        async with self._uow as uow:
            service = await uow.account_repository.create(body, **extra_model_fields)
            await uow.commit()
        return service
    
    async def get_my_account(self, account_id: UUID, user: User):
        async with self._uow as uow:
            if user.role == UserRole.BROKER:
                account = await uow.account_repository.find_by_id(
                    account_id, exception_on_none=True
                )

                if account.broker_id != user.id:
                    raise ForbiddenException("You have not enough permissions")
            
            else:
                if not await uow.user_permission_repository.has_permissions(account_id, user.id):
                    raise ForbiddenException("You have not enough permissions")
                
                account = await uow.account_repository.find_by_id(
                    account_id, exception_on_none=True
                )
        
        account_data = {
            'login': account.login,
            'password': account.password
        }

        account_data_bytes = json.dumps(account_data).encode("utf-8")

        public_key = serialization.load_pem_public_key(
            (await self._redis_cache.get((user.id,))).get("public_key").encode("utf-8")
        )

        encrypted_bytes = public_key.encrypt(
            account_data_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_base64_str = base64.b64encode(encrypted_bytes).decode("utf-8")

        return GetEncryptedAccountData(data=encrypted_base64_str)
    

    async def get_my_accounts(self, user: User):
        async with self._uow as uow:
            if user.role == UserRole.BROKER:
                accounts = await uow.account_repository.find_all(broker_id=user.id)

            else:
                accounts = await uow.account_repository.get_client_accounts_to_services(
                    user.id
                )
        return accounts
        
    async def update_my_account(self, account_id: UUID, body: UpdateAccountDTO):
        async with self._uow as uow:
            account = await uow.account_repository.find_by_id(
                account_id, exception_on_none=True
            )
            updated_account = await uow.account_repository.update(
                db_obj=account, obj_in=body
            )
            await uow.commit()

        return updated_account
    
    async def delete_my_account(self, account_id: UUID):
        async with self._uow as uow:
            await uow.account_repository.delete_by_id(account_id)
            await uow.commit()

        return Response(message="Account was succesfully deleted")
