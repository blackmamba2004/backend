from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

import logging


logger = logging.getLogger(__name__)


class AbstractUnitOfWork(Protocol):
    """
    Абстрактный Unit of Work
    """

    session: AsyncSession | None = None

    def __init__(self):
        pass

    async def __aexit__(self, exc_type: type, exc_value: BaseException, traceback):
        if exc_type == ConnectionRefusedError:
            logger.error(f"The connection to the database has been disconnected")
            await self.rollback()
        elif exc_type is not None:
            await self.rollback()
            logger.debug(f"Exception detection on exit, transaction rollback")

        await self.close()
        logger.debug("Session closed")

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...
