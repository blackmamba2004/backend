from typing import Any

import yaml
import logging

from path import get_logger_config_path


logger = logging.getLogger(__name__)


def read_logger_config() -> dict[str, Any]:
    """
    Для чтения логгера
    """
    with open(get_logger_config_path(), "r") as file:
        return yaml.safe_load(file)


def setup_logger():
    """Настройка логгера приложения"""
    logging.config.dictConfig(read_logger_config())
    logger.info("Logger configured successfully")
