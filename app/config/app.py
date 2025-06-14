from typing import Any

from pydantic_settings import BaseSettings

from .reader import read_config


class AppConfig(BaseSettings):
    """
    Конфиг главного приложения
    """
    project_name: str
    domain: str
    version: str
    debug: bool
    allow_origins: list[str]

    @property
    def root_path(self):
        return self.domain + self.version


def load_app_config() -> AppConfig:
    return AppConfig(
        **read_app_config()
    )


def read_app_config() -> dict[str, Any]:
    return read_config().get("app")
