from fastapi import APIRouter

from api.healthcheck.endpoints import router as healthcheck_router

# Root Router
root_router = APIRouter()
root_router.include_router(healthcheck_router)
