from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth import register_coach, login_coach, register_trainee, login_trainee
from app.schemas.coach import CoachCreate
from app.schemas.trainee import TraineeCreate
from app.schemas.common import TokenResponse, UserType
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/coach/register", response_model=TokenResponse)
async def register_coach_endpoint(coach: CoachCreate, session: AsyncSession = Depends(get_db)):
    new_coach = await register_coach(session, coach.name, coach.email, coach.password, coach.bio, coach.avatar_url)
    access_token = create_access_token({"sub": str(new_coach.id), "type": "coach"})
    return TokenResponse(access_token=access_token, user_type=UserType.COACH)

@router.post("/coach/login", response_model=TokenResponse)
async def login_coach_endpoint(email: str, password: str, session: AsyncSession = Depends(get_db)):
    coach = await login_coach(session, email, password)
    if not coach:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(coach.id), "type": "coach"})
    return TokenResponse(access_token=access_token, user_type=UserType.COACH)

@router.post("/auth/trainee/register", response_model=TokenResponse)
async def register_trainee_endpoint(trainee: TraineeCreate, session: AsyncSession = Depends(get_db)):
    new_trainee = await register_trainee(session, trainee.name, trainee.email, trainee.password)
    access_token = create_access_token({"sub": str(new_trainee.id), "type": "trainee"})
    return TokenResponse(access_token=access_token, user_type=UserType.TRAINEE)

@router.post("/auth/trainee/login", response_model=TokenResponse)
async def login_trainee_endpoint(email: str, password: str, session: AsyncSession = Depends(get_db)):
    trainee = await login_trainee(session, email, password)
    if not trainee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(trainee.id), "type": "trainee"})
    return TokenResponse(access_token=access_token, user_type=UserType.TRAINEE)
