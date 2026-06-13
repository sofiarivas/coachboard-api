from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class CoachCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class CoachResponse(BaseModel):
    id: UUID
    name: str
    email: str
    bio: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
