from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Subscription, Board
from app.schemas.board import BoardResponse
from app.schemas.subscription import SubscriptionResponse
from app.utils.security import decode_token, oauth2_scheme
from uuid import UUID

router = APIRouter(prefix="/boards", tags=["subscriptions"])

@router.post("/{board_id}/subscribe", response_model=SubscriptionResponse)
async def subscribe(board_id: UUID, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "trainee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only trainees can subscribe")
    
    trainee_id = UUID(payload["sub"])
    
    board_result = await session.execute(select(Board).where(Board.id == board_id))
    if not board_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    
    subscription = Subscription(trainee_id=trainee_id, board_id=board_id)
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return subscription

@router.delete("/{board_id}/subscribe")
async def unsubscribe(board_id: UUID, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "trainee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only trainees can unsubscribe")
    
    trainee_id = UUID(payload["sub"])
    result = await session.execute(
        select(Subscription).where(
            (Subscription.trainee_id == trainee_id) & (Subscription.board_id == board_id)
        )
    )
    subscription = result.scalar_one_or_none()
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    
    await session.delete(subscription)
    await session.commit()
    return {"message": "Unsubscribed"}

@router.get("/me/boards", response_model=list[BoardResponse])
async def get_my_boards(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "trainee":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only trainees can view their boards")
    
    trainee_id = UUID(payload["sub"])
    result = await session.execute(
        select(Board)
        .join(Subscription, Subscription.board_id == Board.id)
        .where(Subscription.trainee_id == trainee_id)
    )
    return result.scalars().all()
