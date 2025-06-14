from typing import Any

from .reader import read_config

from pydantic_settings import BaseSettings


class SMTPConfig(BaseSettings):
    """
    Конфиг SMTP-сервера
    """
    tls: int
    host: str
    port: int
    user: str
    password: str

    @property
    def options(self):
        return self.model_dump()


def load_smtp_config() -> SMTPConfig:
    return SMTPConfig(
        **read_smtp_config()
    )


def read_smtp_config() -> dict[str, Any]:
    return read_config().get("smtp")

