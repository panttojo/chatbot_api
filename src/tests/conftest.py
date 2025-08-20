from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from db.postgres.session import async_engine, async_session_factory
from main import app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="function")
async def session():
    async with async_session_factory() as session:
        yield session


@pytest_asyncio.fixture()
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_openai():
    with patch("core.bots.openai.OpenAIBot.chat") as mock_chat:
        mock_response = MagicMock()
        mock_response.output_text = "Test response"
        mock_response.id = "abc-123"
        mock_response.model_dump.return_value = {"id": "abc-123"}

        mock_chat.return_value = mock_response
        yield mock_chat
