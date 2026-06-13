from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class BoardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: str = "public"

class BoardResponse(BaseModel):
    id: UUID
    coach_id: UUID
    name: str
    description: Optional[str]
    visibility: str
    created_at: datetime

    class Config:
        from_attributes = True

class BoardWithWorkouts(BoardResponse):
    workouts: List["WorkoutResponse"] = []
