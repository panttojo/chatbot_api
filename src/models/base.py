import uuid
from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from utils.localtime import LocalTime


class BaseModel(SQLModel, table=False):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4, nullable=False)
    created_at: datetime = Field(default_factory=LocalTime.now, nullable=False, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=LocalTime.now, nullable=False, sa_type=DateTime(timezone=True))

    model_config = ConfigDict(arbitrary_types_allowed=True)
