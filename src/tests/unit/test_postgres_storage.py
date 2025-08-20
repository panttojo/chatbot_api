import pytest

from db.postgres.storage import PostgresStorage
from models.chatbot import Conversation, Message
from models.enums import RoleEnum


@pytest.mark.asyncio
async def test_postgres_storage_save(session) -> None:
    storage = PostgresStorage(session)
    assert storage is not None

    conversation = await storage.save(Conversation())
    assert conversation is not None

    message = await storage.save(Message(message="Test Message", conversation_id=conversation.id, role=RoleEnum.USER))
    assert message is not None


@pytest.mark.asyncio
async def test_postgres_storage_retrieve(session) -> None:
    storage = PostgresStorage(session)
    assert storage is not None

    conversation = await storage.save(Conversation())
    assert conversation is not None

    retrieved_conversation = await storage.retrieve(Conversation, conversation.id)
    assert retrieved_conversation is not None
    assert retrieved_conversation.id == conversation.id


@pytest.mark.asyncio
async def test_postgres_storage_refresh(session) -> None:
    storage = PostgresStorage(session)
    assert storage is not None

    conversation = await storage.save(Conversation())
    assert conversation is not None

    message = await storage.save(Message(message="Test Message", conversation_id=conversation.id, role=RoleEnum.USER))
    assert message is not None

    await storage.refresh(conversation, ["messages"])
    assert conversation.messages is not None
    assert conversation.messages == [message]
