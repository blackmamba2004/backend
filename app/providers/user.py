from dishka import Provider, Scope, provide

from app.models.user import Admin, Broker, Client, AnyUser
from app.service import AuthService


class UserProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_current_admin(
        self, auth_service: AuthService
    ) -> Admin:
        return await auth_service.check_admin_access_token()

    @provide
    async def get_current_broker(
        self, auth_service: AuthService
    ) -> Broker:
        return await auth_service.check_broker_access_token()
    
    @provide
    async def get_current_client(
        self, auth_service: AuthService
    ) -> Client:
        return await auth_service.check_client_access_token()

    @provide
    async def get_current_user(
        self, auth_service: AuthService
    ) -> AnyUser:
        return await auth_service.check_any_access_token()