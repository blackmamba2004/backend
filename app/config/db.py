from typing import Any

from pydantic_settings import BaseSettings

from .reader import read_config


class DBConfig(BaseSettings):
    """
    Конфиг базы данных
    """
    driver: str
    type: str
    user: str
    password: str
    host: str
    port: int
    name: str
    pool_size: int
    max_overflow: int

    @property
    def ASYNC_URI(self):
        return f"{self.type}+{self.driver}://"\
               f"{self.user}:{self.password}@"\
               f"{self.host}:{self.port}/{self.name}"
    @property
    def URI(self):
        return f"{self.type}://"\
               f"{self.user}:{self.password}@"\
               f"{self.host}:{self.port}/{self.name}"


def load_db_config() -> DBConfig:
    return DBConfig(
        **read_db_config()
    )


def read_db_config() -> dict[str, Any]:
    return read_config().get("db")
