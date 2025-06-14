from typing import Any

from pydantic_settings import BaseSettings

from .reader import read_config


class UvicornConfig(BaseSettings):
    """
    Конфиг сервера
    """
    host: str
    port: int


def load_uvicorn_config() -> UvicornConfig:
    return UvicornConfig(
        **read_uvicorn_config()
    )


def read_uvicorn_config() -> dict[str, Any]:
    return read_config().get("uvicorn")
