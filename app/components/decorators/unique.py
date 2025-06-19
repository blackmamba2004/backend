import functools
import logging
from typing import Callable, TypeVar, Awaitable

from sqlalchemy.exc import IntegrityError

from app.components.exceptions.database import UniqueConstraintViolationError

F = TypeVar('F', bound=Callable[..., Awaitable])


logger = logging.getLogger(__name__)


def unique_error(func: F) -> F:
    """
    Декоратор для отлова ошибки нарушения уникальности столбца в базе данных
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Awaitable:
        message_template = kwargs.pop("message", "Record with {field} already exists")
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            logger.debug(f"IntegrityError catched: {e}")
            error_message = str(e)

            if "duplicate key value violates unique" in error_message:
                field_name = None
                if 'Key (' in error_message:
                    field_name = error_message.split('Key (')[1].split(')')[0]

                final_message = message_template.format(field=field_name or "unknown")
                raise UniqueConstraintViolationError(message=final_message) from e

                raise UniqueConstraintViolationError(
                    message=f"Record with {field_name} already exists"
                ) from e
            else:
                logger.error(error_message, exc_info=e)
                raise

    return wrapper
