from uuid import UUID

from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Security

from app.models.user import Admin, AnyUser
from app.routers.auth import api_key_header
from app.routers.tags import (
    serv_admin_tags,
    serv_common_tags
)
from app.schemas.requests import (
    CreateServiceRequest,
    UpdateServiceRequest
)
from app.schemas.responses import GetServiceResponse, Response
from app.service import Service

router = APIRouter(route_class=DishkaRoute)

from logging import getLogger

logger = getLogger(__name__)


@router.post(
    "/services",
    response_model=GetServiceResponse,
    summary="Создает новый сервис",
    description="Создает новый сервис",
    tags=[serv_admin_tags],
)
async def create_service(
    data: CreateServiceRequest,
    _: FromDishka[Admin],
    service: FromDishka[Service],
    authorization = Security(api_key_header),
):
    return await service.create_service(data)


@router.get(
    "/services",
    response_model=list[GetServiceResponse],
    summary="Получает список сервисов",
    description="Получает список сервисов",
    tags=[serv_common_tags],
)
async def get_services(
    _: FromDishka[AnyUser],
    service: FromDishka[Service],
    authorization = Security(api_key_header),
):
    return await service.get_all_services()


@router.get(
    "/services/{service_id}",
    response_model=GetServiceResponse,
    summary="Получает один сервис",
    description="Получает сервис из id в пути запроса",
    tags=[serv_admin_tags],
)
async def get_service(
    service_id: UUID,
    _: FromDishka[Admin],
    service: FromDishka[Service],
    authorization = Security(api_key_header),
):
    return await service.get_service(service_id)


@router.patch(
    "/services/{service_id}",
    response_model=GetServiceResponse,
    summary="Изменяет один сервис",
    description="Изменяет один сервис",
    tags=[serv_admin_tags],
)
async def update_service(
    service_id: UUID,
    data: UpdateServiceRequest,
    _: FromDishka[Admin],
    service: FromDishka[Service],
    authorization = Security(api_key_header),
):
    return await service.update_service(service_id, data)


@router.delete(
    "/services/{service_id}",
    response_model=Response,
    summary="Удаляет один сервис",
    description="Удаляет один сервис",
    tags=[serv_admin_tags],
)
async def update_service(
    service_id: UUID,
    _: FromDishka[Admin],
    service: FromDishka[Service],
    authorization = Security(api_key_header),
):
    return await service.delete_service(service_id)
