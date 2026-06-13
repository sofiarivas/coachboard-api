from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Coach
from app.schemas.coach import CoachResponse
from uuid import UUID

router = APIRouter(prefix="/coaches", tags=["coaches"])

@router.get("", response_model=list[CoachResponse])
async def list_coaches(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Coach))
    return result.scalars().all()

@router.get("/{coach_id}", response_model=CoachResponse)
async def get_coach(coach_id: UUID, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Coach).where(Coach.id == coach_id))
    coach = result.scalar_one_or_none()
    if not coach:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coach not found")
    return coach
