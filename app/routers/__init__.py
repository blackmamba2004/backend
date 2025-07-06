from fastapi import APIRouter

from app.routers import (
    auth, service
)


def api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth.router)
    router.include_router(service.router)
    return router
