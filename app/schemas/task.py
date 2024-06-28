import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskStatus(str, enum.Enum):
    pending = "pending"
    refining = "refining"
    doing = "doing"
    approving = "approving"
    completed = "completed"


class TaskBase(BaseModel):
    title: str
    status: TaskStatus


class TaskCreate(TaskBase):
    owner_id: Optional[uuid.UUID] = None
    assigned_user_id: Optional[uuid.UUID] = None
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_user_id: Optional[uuid.UUID] = None


class TaskInDB(TaskBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    assigned_user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class Task(TaskInDB):
    pass
