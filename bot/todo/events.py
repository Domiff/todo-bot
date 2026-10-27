from datetime import datetime

from pydantic import BaseModel, ConfigDict

TASK_CREATED_EVENT_TYPE = "todo.task.created.v1"


class TaskCreatedData(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: int
    tg_id: int
    title: str
    deadline: datetime
