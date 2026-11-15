from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class TaskEventTypes(StrEnum):
    CREATED_EVENT = "todo.task.created.v1"
    UPDATED_EVENT = "todo.task.updated.v1"
    DELETED_EVENT = "todo.task.deleted.v1"


class ChangedVia(StrEnum):
    WEB = "web"
    TELEGRAM = "telegram"


class TaskData(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: int
    user_id: int | None = None
    tg_id: int | None
    changed_via: ChangedVia = ChangedVia.WEB
    title: str
    body: str = ""
    completed: bool = False
    deadline: datetime | None = None
    priority: int = 2
    category: str = ""
