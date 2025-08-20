import uuid

import pytest
from fastapi.testclient import TestClient

from db.postgres.session import async_session_factory
from models.chatbot import Conversation, Message


def test_chatbot_endpoint(client: TestClient, mock_openai):
    user_message = "Hello, how are you?"
    response = client.post("/v1/chat", json={"message": user_message})
    response_json = response.json()

    assert response.status_code == 201
    assert response_json is not None
    assert response_json["messages"] is not None
    assert len(response_json["messages"]) == 2
    assert response_json["messages"][0]["message"] == user_message
    assert response_json["messages"][0]["role"] == "user"
    assert response_json["messages"][1]["message"] == "Test response"
    assert response_json["messages"][1]["role"] == "bot"


def test_chatbot_endpoint_with_not_found_conversation_id(client: TestClient, mock_openai):
    user_message = "Hello, how are you?"
    response = client.post("/v1/chat", json={"message": user_message, "conversation_id": str(uuid.uuid4())})
    response_json = response.json()

    assert response.status_code == 404
    assert response_json is not None
    assert response_json["detail"] == "Conversation not found"


@pytest.mark.asyncio
async def test_chatbot_endpoint_with_conversation_id(client: TestClient, mock_openai):
    async with async_session_factory() as session:
        previous_conversation = Conversation(messages=[Message(message="Hello, how are you?", role="user")])
        session.add(previous_conversation)
        await session.commit()

    response = client.post(
        "/v1/chat", json={"message": "Have a nice day!", "conversation_id": str(previous_conversation.id)}
    )
    response_json = response.json()

    assert response.status_code == 201
    assert response_json is not None
    assert response_json["messages"] is not None
    assert len(response_json["messages"]) == 3
    assert response_json["messages"][0]["message"] == "Hello, how are you?"
    assert response_json["messages"][0]["role"] == "user"
    assert response_json["messages"][1]["message"] == "Have a nice day!"
    assert response_json["messages"][1]["role"] == "user"
    assert response_json["messages"][2]["message"] == "Test response"
    assert response_json["messages"][2]["role"] == "bot"


def test_endpoint_with_invalid_payload(client: TestClient, mock_openai):
    response = client.post("/v1/chat", json={"conversation_id": "Hello, how are you?"})
    response_json = response.json()

    assert response.status_code == 422
    assert response_json is not None
    assert response_json["detail"][0]["loc"] == ["body", "message"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"


def test_endpoint_with_message_too_long(client: TestClient, mock_openai):
    response = client.post("/v1/chat", json={"message": "a" * 1001})
    response_json = response.json()

    assert response.status_code == 422
    assert response_json is not None

    assert response_json["detail"][0]["loc"] == ["body", "message"]
    assert response_json["detail"][0]["msg"] == "Message length must be less than 1000 characters"
    assert response_json["detail"][0]["type"] == "value_error"
