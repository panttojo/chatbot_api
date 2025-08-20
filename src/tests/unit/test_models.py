import pytest

from models.chatbot import Conversation, Message
from models.enums import RoleEnum


@pytest.mark.asyncio
async def test_create_conversation(session) -> None:
    conv = Conversation()
    session.add(conv)
    await session.commit()
    await session.refresh(conv, ["messages"])

    assert conv.id is not None
    assert conv.messages == []


@pytest.mark.asyncio
async def test_create_message(session) -> None:
    # Crear conversación primero
    conv = Conversation()
    session.add(conv)
    await session.commit()
    await session.refresh(conv)

    msg_data = {
        "role": RoleEnum.USER,
        "message": "Hola mundo",
        "extra_data": {"id": "123"},
        "conversation_id": conv.id,
    }

    msg = Message(**msg_data)
    session.add(msg)
    await session.commit()
    await session.refresh(msg)

    assert msg.id is not None
    assert msg.role == RoleEnum.USER
    assert msg.message == "Hola mundo"
    assert msg.extra_data == {"id": "123"}
    assert msg.conversation_id == conv.id


@pytest.mark.asyncio
async def test_conversation_messages_relationship(session) -> None:
    conv = Conversation()
    session.add(conv)
    await session.commit()
    await session.refresh(conv)

    # Crear varios mensajes
    msg1 = Message(role=RoleEnum.USER, message="Msg 1", conversation_id=conv.id)
    msg2 = Message(role=RoleEnum.BOT, message="Msg 2", conversation_id=conv.id)
    session.add_all([msg1, msg2])
    await session.commit()

    # Recargar la conversación para obtener mensajes
    await session.refresh(conv, ["messages"])
    messages = conv.messages

    assert len(messages) == 2
    assert messages[0].message == "Msg 1"
    assert messages[1].message == "Msg 2"
