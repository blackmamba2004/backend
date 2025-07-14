from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Security
from fastapi.security.api_key import APIKeyHeader

from app.routers.tags import (
    auth,
    reg,
    admin,
    broker,
    client,
)
from app.service import AuthService
from app.schemas.requests import (
    RegisterBrokerRequest, 
    LoginRequest, 
    LogoutRequest,
    EmailTokenRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
    RegisterUserRequest
)
from app.schemas.responses import TokenPairResponse, Response


router = APIRouter(route_class=DishkaRoute)


api_key_header = APIKeyHeader(
    name="Authorization", description="Bearer <access_token>", auto_error=False
)


@router.post(
    "/brokers/register", 
    response_model=Response,
    summary="Регистрация брокера",
    description="Создает нового пользователя в системе. "
    "После регистрации отправляется письмо на email для подтверждения.",
    tags=[reg, broker]
)
async def register_broker(
    data: RegisterBrokerRequest,
    auth_service: FromDishka[AuthService]
):
    return await auth_service.register_broker(data)


@router.post(
    "/users/invite",
    response_model=Response, 
    summary="Приглашение пользователя",
    description="Создает личную ссылку брокера",
    tags=[reg, client]
)
async def invite_user(
    auth_service: FromDishka[AuthService],
    authorization = Security(api_key_header)
):
    broker = await auth_service.check_broker_access_token()
    return await auth_service.invite_user(broker)


@router.post(
    "/users/register", 
    response_model=Response, 
    summary="Регистрация пользователя",
    description="Создает нового пользователя в системе. "
    "После регистрации отправляется письмо на email для подтверждения.",
    tags=[reg, client]
)
async def register_user(
    auth_service: FromDishka[AuthService],
    data: RegisterUserRequest,
):
    return await auth_service.register_user(data)


@router.post(
    "/login",
    summary="Вход в приложение",
    response_model=TokenPairResponse, 
    description="Выдать access-token и "
    "refresh-token для входа в приложение",
    tags=[auth, admin, broker, client]
)
async def login_user(
    auth_service: FromDishka[AuthService],
    data: LoginRequest,
):
    return await auth_service.login(data)


@router.post(
    "/logout", 
    response_model=Response,
    summary="Выход из приложения",
    description="Требуется refresh-токен",
    tags=[auth, admin, broker, client]
)
async def logout(
    auth_service: FromDishka[AuthService],
    data: LogoutRequest,
):
    return await auth_service.logout(data.refresh_token)


@router.post(
    "/refresh", 
    response_model=TokenPairResponse, 
    summary="Обновить пару токенов",
    description="Для обновления требуется refresh-токен",
    tags=[auth, admin, broker, client]
)
async def refresh_token(
    auth_service: FromDishka[AuthService],
    data: RefreshTokenRequest,
):
    return await auth_service.refresh_tokens(data.refresh_token)


@router.post(
    "/reset-password", 
    response_model=Response,
    summary="Сброс пароля",
    description="Если аккаунт активен"
    "на email отправляется письмо для смены пароля",
    tags=[auth, broker, client]
)
async def reset_password(
    auth_service: FromDishka[AuthService],
    data: ChangePasswordRequest
):
    return await auth_service.reset_password(data.email)


@router.patch(
    "/reset-password/confirm", 
    response_model=Response, 
    summary="Сброс пароля",
    description="Подтвердить сброс пароля и создать новый",
    tags=[auth, broker, client]
)
async def reset_password_confirm(
    auth_service: FromDishka[AuthService],
    data: ResetPasswordRequest
):
    return await auth_service.reset_password_confirm(data)


@router.patch(
    "/verify-email", 
    response_model=Response,
    summary="Подтвердить почту",
    description="После подтверждения почты аккаунт становится активным",
    tags=[reg, broker, client]
)
async def verify_email(
    auth_service: FromDishka[AuthService],
    data: EmailTokenRequest
):
    return await auth_service.verify_email(data.email_token)
