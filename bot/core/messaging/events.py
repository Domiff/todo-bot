from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Event[DataT: BaseModel](BaseModel):
    model_config = ConfigDict(frozen=True)

    specversion: str
    id: UUID
    source: str
    type: str
    time: datetime
    subject: str | None = None
    datacontenttype: str
    data: DataT

    @classmethod
    def from_bytes(cls, body: bytes) -> "Event[DataT]":
        return cls.model_validate_json(body)


class _EventType(BaseModel):
    type: str


def get_event_type(body: bytes) -> str:
    return _EventType.model_validate_json(body).type
