import datetime
import uuid
from typing import ClassVar

from sqlalchemy import DateTime, func, types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from utils.localtime import LocalTime


class Base(DeclarativeBase):
    type_annotation_map: ClassVar = {
        datetime.date: types.Date(),
        datetime.datetime: types.DateTime(timezone=True),
        DateTime: types.DateTime(timezone=True),
    }


class BaseModel(Base):
    __abstract__: ClassVar[bool] = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(default=LocalTime.now, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=LocalTime.now, server_default=func.now(), onupdate=func.now(), server_onupdate=func.now()
    )
