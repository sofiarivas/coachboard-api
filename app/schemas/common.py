from pydantic import BaseModel
from enum import Enum

class UserType(str, Enum):
    COACH = "coach"
    TRAINEE = "trainee"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_type: UserType
