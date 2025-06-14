from dishka import Provider, Scope, provide

from app.components import JWT, RedisCache
from app.config import AppConfig, SMTPConfig
from app.service import AuthService, EmailService, LinkerService
from app.unit_of_work import AuthUnitOfWork


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_auth_service(
        self, 
        auth_unit_of_work: AuthUnitOfWork, 
        email_service: EmailService,
        linker_service: LinkerService,
        redis_cache: RedisCache,
        jwt: JWT
    ) -> AuthService:
        return AuthService(
            auth_unit_of_work, email_service, linker_service, redis_cache, jwt
        )
    
    @provide(scope=Scope.APP)
    def get_email_service(self, smtp_config: SMTPConfig, app_config: AppConfig) -> EmailService:
        return EmailService(smtp_config, app_config.project_name)
    
    @provide(scope=Scope.APP)
    def get_linker_service(self) -> LinkerService:
        return LinkerService()
