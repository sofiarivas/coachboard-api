from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class TraineeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class TraineeResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
