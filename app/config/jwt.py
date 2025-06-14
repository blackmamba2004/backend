from typing import Any

from pydantic_settings import BaseSettings

from .reader import read_config


class JWTConfig(BaseSettings):
    """
    Конфиг JWT
    """
    secret_key: str
    algorithm: str
    access_token_ttl: int
    refresh_token_ttl: int
    email_token_ttl: int
    invite_token_ttl: int


def load_jwt_config() -> JWTConfig:
    return JWTConfig(
        **read_jwt_config()
    )


def read_jwt_config() -> dict[str, Any]:
    return read_config().get("jwt")
