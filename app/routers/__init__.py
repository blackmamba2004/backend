from fastapi import APIRouter

from app.routers import auth


def api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(auth.router)
    return router
