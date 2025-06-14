from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.components.types import AsyncSessionFactory
from app.config import DBConfig
from app.session_factory import initialize_session_factory


class SessionProvider(Provider):
    scope = Scope.APP

    @provide
    def get_async_session_factory(
        self, db_config: DBConfig
    ) -> AsyncSessionFactory:
        return initialize_session_factory(db_config)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self, async_session_factory: AsyncSessionFactory
    ) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as session:
            yield session
