from uuid import UUID
from logging import getLogger

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Security

from app.models.user import Broker, BrokerOrClient
from app.routers.auth import api_key_header
from app.routers.tags import (
    acc,
    broker,
    client
)
from app.schemas.requests import (
    CreateAccountRequest,
    UpdateAccountRequest
)
from app.schemas.responses import (
    GetAccountResponse, 
    GetEncryptedAccountData, 
    Response
)
from app.service import AccountService

router = APIRouter(route_class=DishkaRoute)

logger = getLogger(__name__)


@router.post(
    "/services/{service_id}/accounts",
    response_model=GetAccountResponse,
    summary="Создает новый аккаунт",
    description="Создает новый аккаунт для входа в сервис",
    tags=[acc, broker],
)
async def create_account(
    data: CreateAccountRequest,
    service_id: UUID, 
    broker: FromDishka[Broker],
    service: FromDishka[AccountService],
    authorization = Security(api_key_header),
):
    return await service.create_account(
        data, broker_id=broker.id, service_id=service_id
    )

@router.get(
    "/accounts",
    response_model=list[GetAccountResponse],
    summary="Получает список своих аккаунтов",
    description="Брокер получает список своих аккаунтов, "\
                "а его клиент список доступных аккаунтов",
    tags=[acc, broker, client],
)
async def get_accounts(
    user: FromDishka[BrokerOrClient],
    service: FromDishka[AccountService],
    authorization = Security(api_key_header),
):
    return await service.get_my_accounts(user)

@router.get(
    "/accounts/{account_id}",
    response_model=GetEncryptedAccountData,
    summary="Получает аккаунт",
    description="Получает данные для входа в аккаунт в зашфированном виде",
    tags=[acc, broker, client],
)
async def get_account(
    user: FromDishka[BrokerOrClient],
    account_id: UUID, 
    service: FromDishka[AccountService],
    authorization = Security(api_key_header),
):
    return await service.get_my_account(account_id, user)


@router.patch(
    "/accounts/{account_id}",
    response_model=GetAccountResponse,
    summary="Изменяет данные аккаунта",
    description="Изменяет данные аккаунта для входа в сервис",
    tags=[acc, broker],
)
async def update_account(
    account_id: UUID,
    data: UpdateAccountRequest,
    broker: FromDishka[Broker],
    service: FromDishka[AccountService],
    authorization = Security(api_key_header),
):
    return await service.update_my_account(account_id, data)


@router.delete(
    "/accounts/{account_id}",
    response_model=Response,
    summary="Удаляет один аккаунт",
    description="Удаляет один аккаунт для входа в сервис",
    tags=[acc, broker],
)
async def delete_account(
    account_id: UUID,
    _: FromDishka[Broker],
    service: FromDishka[AccountService],
    authorization = Security(api_key_header),
):
    return await service.delete_my_account(account_id)
