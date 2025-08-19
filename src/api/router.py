from fastapi import APIRouter

from api.healthcheck.endpoints import router as healthcheck_router
from api.v1.chatbot.endpoints import router as chatbot_router

# Root Router
root_router = APIRouter()
root_router.include_router(healthcheck_router)

# API v1 Router
api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(chatbot_router)
