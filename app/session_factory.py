from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, 
    async_sessionmaker,
)

from app.config import DBConfig
from app.components.types import AsyncSessionFactory


def initialize_session_factory(db_config: DBConfig) -> AsyncSessionFactory:
    engine = create_async_engine(
        db_config.ASYNC_URI,
        echo=True,
        future=True,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=db_config.pool_size,
        max_overflow=db_config.max_overflow,
    )
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    return session_factory