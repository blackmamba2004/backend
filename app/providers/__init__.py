from dishka import Provider

from .cache import RedisCacheProvider
from .config import ConfigProvider
from .service import ServiceProvider
from .session import SessionProvider
from .unit_of_work import UnitOfWorkProvider


def provider_list() -> list[Provider]:
    return [
        RedisCacheProvider(),
        ConfigProvider(),
        ServiceProvider(),
        SessionProvider(),
        UnitOfWorkProvider()
    ]
