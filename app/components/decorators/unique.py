import functools
import logging
from typing import Callable, TypeVar, Awaitable, Type

from sqlalchemy.exc import IntegrityError

from app.components.exceptions import ApplicationException

F = TypeVar('F', bound=Callable[..., Awaitable])


logger = logging.getLogger(__name__)


def unique_error(error_class: Type[ApplicationException]):
    """
    Параметризованный декоратор: ловит ошибки уникальности и поднимает переданный тип исключения
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Awaitable:
            try:
                return await func(*args, **kwargs)
            except IntegrityError as e:
                logger.debug(f"IntegrityError catched: {e}")
                error_message = str(e)

                if "duplicate key value violates unique" in error_message:
                    if 'Key (' in error_message:
                        field_name = error_message.split('Key (')[1].split(')')[0]
                        final_message = f"This {field_name} is taken"
                    
                    raise error_class(message=final_message) from e
                
                else:
                    logger.error(error_message, exc_info=e)
                    raise

        return wrapper
    
    return decorator
