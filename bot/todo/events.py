from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class TaskEventTypes(StrEnum):
    CREATED_EVENT = "todo.task.created.v1"
    UPDATED_EVENT = "todo.task.updated.v1"
    DELETED_EVENT = "todo.task.deleted.v1"


class BaseTaskData(BaseModel):
    model_config = ConfigDict(frozen=True)


class TaskCreatedData(BaseTaskData):
    task_id: int
    tg_id: int
    title: str
    deadline: datetime


class TaskUpdatedData(BaseTaskData):
    task_id: int
    tg_id: int
    title: str
    body: str
    completed: bool
    deadline: datetime
    category: str


class TaskDeletedData(BaseTaskData):
    task_id: int
    tg_id: int
    title: str
