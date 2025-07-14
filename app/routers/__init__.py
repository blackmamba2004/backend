from fastapi import APIRouter

from app.routers import (
    account, auth, service, user
)


def api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(account.router)
    router.include_router(auth.router)
    router.include_router(service.router)
    router.include_router(user.router)
    return router
