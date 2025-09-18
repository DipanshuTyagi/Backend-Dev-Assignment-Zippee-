from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True  # enable from ORM-like objects
    }
