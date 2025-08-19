from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
