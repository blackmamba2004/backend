from dishka import Provider, Scope, provide
from fastapi import Request

from app.components import JWT, RedisCache
from app.config import AppConfig, SMTPConfig
from app.service import (
    AccountService, 
    AuthService, 
    EmailService, 
    LinkerService, 
    Service,
    UserService
)
from app.unit_of_work import (
    AccountUnitOfWork, 
    AuthUnitOfWork, 
    ServiceUnitOfWork,
    UserUnitOfWork
)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_auth_service(
        self, 
        auth_unit_of_work: AuthUnitOfWork, 
        email_service: EmailService,
        linker_service: LinkerService,
        redis_cache: RedisCache,
        jwt: JWT,
        request: Request
    ) -> AuthService:
        return AuthService(
            auth_unit_of_work, 
            email_service, 
            linker_service, 
            redis_cache, 
            jwt,
            request
        )

    @provide
    def get_account_service(
        self, account_unit_of_work: AccountUnitOfWork, redis_cache: RedisCache,
    ) -> AccountService:
        return AccountService(account_unit_of_work, redis_cache)
    
    @provide(scope=Scope.APP)
    def get_email_service(
        self, smtp_config: SMTPConfig, app_config: AppConfig
    ) -> EmailService:
        return EmailService(smtp_config, app_config.project_name)
    
    @provide(scope=Scope.APP)
    def get_linker_service(self) -> LinkerService:
        return LinkerService()
    
    @provide
    def get_service(self, unit_of_work: ServiceUnitOfWork) -> Service:
        return Service(unit_of_work)
    
    @provide
    async def get_request(self) -> Request:
        return Request()
    
    @provide
    def get_user_service(
        self, unit_of_work: UserUnitOfWork,
    ) -> UserService:
        return UserService(unit_of_work)