from dishka import Provider, Scope, provide

from app.models.user import Admin, AnyUser, Broker, BrokerOrClient, Client
from app.service import AuthService


class UserProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_current_admin(
        self, auth_service: AuthService
    ) -> Admin:
        return await auth_service.check_admin_access_token()

    @provide
    async def get_current_any_user(
        self, auth_service: AuthService
    ) -> AnyUser:
        return await auth_service.check_any_access_token()

    @provide
    async def get_current_broker(
        self, auth_service: AuthService
    ) -> Broker:
        return await auth_service.check_broker_access_token()
    
    @provide
    async def get_current_broker_or_client(
        self, auth_service: AuthService
    ) -> BrokerOrClient:
        return await auth_service.check_broker_or_client_access_token()
    
    @provide
    async def get_current_client(
        self, auth_service: AuthService
    ) -> Client:
        return await auth_service.check_client_access_token()
