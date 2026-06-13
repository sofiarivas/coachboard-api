from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any

class WorkoutCreate(BaseModel):
    title: str
    scheduled_at: datetime
    status: str = "draft"
    content: Optional[dict] = None

class WorkoutResponse(BaseModel):
    id: UUID
    board_id: UUID
    title: str
    scheduled_at: datetime
    status: str
    content: Optional[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkoutUpdate(BaseModel):
    title: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    content: Optional[dict] = None
