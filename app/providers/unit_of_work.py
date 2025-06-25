from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import UserRepository
from app.unit_of_work import AuthUnitOfWork


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
