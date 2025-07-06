from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import UserRepository, ServiceRepository
from app.unit_of_work import AuthUnitOfWork, ServiceUnitOfWork


class UnitOfWorkProvider(Provider):
    scope = Scope.REQUEST
    
    @provide
    def get_auth_unit_of_work(
        self, async_session: AsyncSession
    ) -> AuthUnitOfWork:
        return AuthUnitOfWork(
            session=async_session,
            repository_list=[
                UserRepository()
            ]
        )

    @provide
    def get_service_unit_of_work(
        self, async_session: AsyncSession
    ) -> ServiceUnitOfWork:
        return ServiceUnitOfWork(
            session=async_session,
            repository_list=[
                ServiceRepository()
            ]
        )
