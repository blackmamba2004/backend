from logging import getLogger
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Security

from app.models.user import Broker
from app.routers.auth import api_key_header
from app.routers.tags import (
    broker
)

from app.service import UserService
from app.schemas.requests import ChangeUserPermissionsRequest
from app.schemas.responses import Response

router = APIRouter(route_class=DishkaRoute)

logger = getLogger(__name__)


@router.get(
    "/users",
    tags=[broker],
)
async def users(
    broker: FromDishka[Broker],
    service: FromDishka[UserService],
    authorization = Security(api_key_header),
):
    return await service.get_my_clients(broker)


@router.patch(
    "/accounts/{account_id}/permissions/{user_id}",
    response_model=Response, 
    tags=[broker],
)
async def change_user_permissions(
    account_id: UUID,
    user_id: UUID,
    body: ChangeUserPermissionsRequest,
    broker: FromDishka[Broker],
    service: FromDishka[UserService],
    authorization = Security(api_key_header),
):
    return await service.change_user_permissions(
        broker.id, account_id, user_id, body
    )
