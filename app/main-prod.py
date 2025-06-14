import logging

from uvicorn import run

from app.app_factory import init_app
from app.config import load_uvicorn_config
from app.logger import setup_logger


logger = logging.getLogger(__name__)


setup_logger()
app = init_app()
config = load_uvicorn_config()

if __name__ == "__main__":
    run(
        app=app,
        host=config.host, 
        port=config.port
    )
