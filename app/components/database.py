import asyncio
import logging

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text, AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session, async_sessionmaker,
)

from app.config import DBConfig


logger = logging.getLogger(__name__)


#TODO: прокидывать в провайдер вместо AsyncSession
class AsyncDatabase:
    """
    Класс для асинхронной работы с базой данных с поддержкой переподключения.
    """
    def __init__(self, config: DBConfig):
        self._config = config
        self._initialize_engine_and_session()

    def _initialize_engine_and_session(self):
        """Инициализирует движок и фабрику сессий"""
        self._engine = create_async_engine(
            self._config.ASYNC_URI,
            echo=True,
            future=True,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=self._config.pool_size,
            max_overflow=self._config.max_overflow,
        )
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        self._session_factory = async_scoped_session(
            self._session_maker,
            asyncio.current_task
        )

    async def reconnect(self, retries: int = 5, delay: float = 2.0) -> None:
        """
        Переподключение к базе данных при потере соединения.

        :param retries: Количество попыток переподключения.
        :param delay: Задержка между попытками в секундах.
        """
        for attempt in range(retries):
            try:
                logger.debug(f"An attempt to connect to the database ({attempt + 1}/{retries})...")
                self._initialize_engine_and_session()
                async with self._engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("The connection to the database has been successfully restored.")
                return
            except ConnectionRefusedError as e:
                logger.warning(f"Database connection error: {e}. Attempt {attempt + 1} from {retries}.")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    logger.error("The connection to the database could not be restored.")
                    raise RuntimeError("The connection to the database could not be restored.")

    @asynccontextmanager
    async def session(self, with_commit=False) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронный менеджер контекста для сессии с обработкой потери соединения.
        """
        session: AsyncSession = self._session_factory(autocommit=False)
        try:
            yield session
            if with_commit:
                await session.commit()
        except ConnectionRefusedError as e:
            logger.error("An error occurred in the session, the connection to the database may have been lost.")
            await self.reconnect()
            raise
        except Exception:
            logger.debug("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            logger.debug(f"Session {id(session)} closed.")
            await session.close()
            await self._session_factory.remove()
            logger.debug("Session closed")

    async def create_session(self) -> AsyncSession:
        """
        Создать экземпляр сессии без контекстного менеджера
        """
        return self._session_factory(autocommit=False)

    async def close_session(self, session: AsyncSession) -> None:
        """
        Закрыть сессию и удалить её из реестра фабрики
        :param session:
        :return:
        """
        await session.close()
        await self._session_factory.remove()
