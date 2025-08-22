import uuid

import pytest

from api.v1.chatbot.schemas import CreateMessageSchema
from api.v1.chatbot.services import ChatbotService
from api.v1.exceptions import NotFoundException
from models.enums import RoleEnum


@pytest.mark.asyncio
async def test_chatbot_service(session, mock_openai_chat, mock_openai_create_conversation):
    service = ChatbotService(session=session)
    assert service is not None

    user_message = "Hello, how are you?"
    payload = CreateMessageSchema(message=user_message, role=RoleEnum.USER)
    conversation = await service.handle_message(payload)

    assert conversation is not None
    assert conversation.messages is not None
    assert len(conversation.messages) == 2
    assert conversation.messages[0].message == user_message
    assert conversation.messages[0].role == RoleEnum.USER

    assert conversation.messages[1].message == "Test response"
    assert conversation.messages[1].role == RoleEnum.BOT
    assert conversation.messages[1].extra_data["id"] == "abc-123"


@pytest.mark.asyncio
async def test_chatbot_service_retrieve_conversation(session, mock_openai_chat, mock_openai_create_conversation):
    service = ChatbotService(session=session)
    assert service is not None

    payload = CreateMessageSchema(message="Hello, how are you?", role=RoleEnum.USER)
    conversation = await service.handle_message(payload)

    retrieved_conversation = await service.retrieve_conversation(conversation.id)
    assert retrieved_conversation is not None
    assert retrieved_conversation.id == conversation.id
    assert len(retrieved_conversation.messages) == 2


@pytest.mark.asyncio
async def test_chatbot_service_retrieve_conversation_not_found(
    session, mock_openai_chat, mock_openai_create_conversation
):
    service = ChatbotService(session=session)
    assert service is not None

    with pytest.raises(NotFoundException):
        await service.retrieve_conversation(uuid.uuid4())


@pytest.mark.asyncio
async def test_chatbot_service_save_message(session, mock_openai_chat, mock_openai_create_conversation):
    service = ChatbotService(session=session)
    assert service is not None

    payload = CreateMessageSchema(message="Hello, how are you?", role=RoleEnum.USER)
    conversation = await service.handle_message(payload)

    assert conversation is not None
    assert len(conversation.messages) == 2


@pytest.mark.asyncio
async def test_chatbot_service_get_previous_response_id(session, mock_openai_chat, mock_openai_create_conversation):
    service = ChatbotService(session=session)
    assert service is not None

    payload = CreateMessageSchema(message="Hello, how are you?", role=RoleEnum.USER)
    conversation = await service.handle_message(payload)

    assert conversation is not None
    assert len(conversation.messages) == 2
    assert conversation.messages[1].role == RoleEnum.BOT
    assert conversation.messages[1].extra_data["id"] == "abc-123"
