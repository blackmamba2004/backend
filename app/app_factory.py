import logging

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import AppConfig, load_app_config
from app.container import create_container
from app.components.exceptions import ApplicationException, application_exception_handler
from app.routers import api_router


logger = logging.getLogger(__name__)


def create_app(config: AppConfig) -> FastAPI:
    app = FastAPI(
        root_path=config.root_path,
        debug=config.debug,
        exception_handlers={
            ApplicationException: application_exception_handler
        }
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.allow_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router())
    return app

def init_app():
    container = create_container()
    
    api_config = load_app_config()

    app = create_app(api_config)

    setup_dishka(container, app)

    logger.info("FastAPI started")

    return app
