import logging

from app.loader import load_config


logger = logging.getLogger(__name__)


def setup_logger():
    """Настройка логгера приложения"""
    logging.config.dictConfig(load_config("LOGGER_CONFIG_PATH"))
    logger.info("Logger configured successfully")
