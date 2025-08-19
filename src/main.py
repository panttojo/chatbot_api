from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from core.settings import settings
from core.utils.environment import EnvironmentEnum
from db.postgres.session import init_db, test_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
    await test_db_connection()

    # Only initialize the database in local and testing environment
    if settings.ENVIRONMENT in [EnvironmentEnum.LOCAL, EnvironmentEnum.TESTING]:
        await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router.root_router)
    app.include_router(router.api_v1_router)

    return app


app = create_app()
