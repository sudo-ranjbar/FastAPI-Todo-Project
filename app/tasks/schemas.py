from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(
        ..., max_length=150, min_length=5, description="Title of the task"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Task's description"
    )
    is_complete: bool = Field(..., description="Status of the task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")
    created_at: datetime = Field(..., description="Time of creation")
    updated_at: datetime = Field(..., description="Time of update")
