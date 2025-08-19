from fastapi import APIRouter, status

from .schemas import HealthcheckSchema

router = APIRouter(prefix="/health", tags=["Healthcheck"])


@router.get("", status_code=status.HTTP_200_OK)
async def healthcheck() -> HealthcheckSchema:
    return HealthcheckSchema()
