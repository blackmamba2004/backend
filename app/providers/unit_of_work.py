from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import (
    AccountRepository, 
    ServiceRepository, 
    UserRepository,
    UserPermissionRepository
)
from app.unit_of_work import (
    AccountUnitOfWork, 
    AuthUnitOfWork, 
    ServiceUnitOfWork, 
    UserUnitOfWork
)


class UnitOfWorkProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_account_unit_of_work(
        self, async_session: AsyncSession
    ) -> AccountUnitOfWork:
        return AccountUnitOfWork(
            session=async_session,
            repository_list=[
                AccountRepository(),
                UserPermissionRepository()
            ]
        )
    
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
    
    @provide
    def get_user_unit_of_work(
        self, async_session: AsyncSession
    ) -> UserUnitOfWork:
        return UserUnitOfWork(
            session=async_session,
            repository_list=[
                UserRepository()
            ]
        )