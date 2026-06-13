from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Workout, Board
from app.schemas.workout import WorkoutCreate, WorkoutResponse, WorkoutUpdate
from app.services.workout import get_today_workouts, get_upcoming_workouts
from app.utils.security import decode_token, oauth2_scheme
from uuid import UUID

router = APIRouter(tags=["workouts"])

@router.get("/workouts/{workout_id}", response_model=WorkoutResponse)
async def get_workout(workout_id: UUID, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Workout).where(Workout.id == workout_id))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    return workout

@router.get("/today", response_model=list[WorkoutResponse])
async def get_today(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "trainee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only trainees can view workouts")
    
    trainee_id = UUID(payload["sub"])
    workouts = await get_today_workouts(session, trainee_id)
    return workouts

@router.get("/upcoming", response_model=list[WorkoutResponse])
async def get_upcoming(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "trainee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only trainees can view workouts")
    
    trainee_id = UUID(payload["sub"])
    workouts = await get_upcoming_workouts(session, trainee_id)
    return workouts

@router.post("/boards/{board_id}/workouts", response_model=WorkoutResponse)
async def create_workout(board_id: UUID, workout: WorkoutCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "coach":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only coaches can create workouts")
    
    board_result = await session.execute(select(Board).where(Board.id == board_id))
    board = board_result.scalar_one_or_none()
    if not board or str(board.coach_id) != payload["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Board not found or unauthorized")
    
    new_workout = Workout(board_id=board_id, **workout.dict())
    session.add(new_workout)
    await session.commit()
    await session.refresh(new_workout)
    return new_workout

@router.put("/workouts/{workout_id}", response_model=WorkoutResponse)
async def update_workout(workout_id: UUID, workout: WorkoutUpdate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "coach":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only coaches can update workouts")
    
    result = await session.execute(select(Workout).where(Workout.id == workout_id))
    db_workout = result.scalar_one_or_none()
    if not db_workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    
    board_result = await session.execute(select(Board).where(Board.id == db_workout.board_id))
    board = board_result.scalar_one_or_none()
    if str(board.coach_id) != payload["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    update_data = workout.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_workout, field, value)
    
    await session.commit()
    await session.refresh(db_workout)
    return db_workout
