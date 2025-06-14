from typing import Any

from pydantic_settings import BaseSettings

from .reader import read_config


class RedisConfig(BaseSettings):
    """
    Конфиг Redis
    """
    name: str
    host: str
    port: int
    cache_ttl: int

    @property
    def URI(self):
        return f"{self.name}://{self.host}:{self.port}"


def load_redis_config() -> RedisConfig:
    return RedisConfig(
        **read_redis_config()
    )


def read_redis_config() -> dict[str, Any]:
    return read_config().get("redis")
