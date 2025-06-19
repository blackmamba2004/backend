import logging

from app.app_factory import init_app
from app.logger import setup_logger


logger = logging.getLogger(__name__)


setup_logger()
app = init_app()
