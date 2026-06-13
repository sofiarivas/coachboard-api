from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class SubscriptionResponse(BaseModel):
    id: UUID
    trainee_id: UUID
    board_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
