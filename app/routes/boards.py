from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Board, Coach
from app.schemas.board import BoardCreate, BoardResponse
from app.utils.security import decode_token, oauth2_scheme
from uuid import UUID

router = APIRouter(prefix="/boards", tags=["boards"])

@router.get("", response_model=list[BoardResponse])
async def list_boards(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Board).where(Board.visibility == "public"))
    return result.scalars().all()

@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(board_id: UUID, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Board).where(Board.id == board_id))
    board = result.scalar_one_or_none()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return board

@router.post("", response_model=BoardResponse)
async def create_board(board: BoardCreate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "coach":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only coaches can create boards")
    
    new_board = Board(coach_id=UUID(payload["sub"]), **board.dict())
    session.add(new_board)
    await session.commit()
    await session.refresh(new_board)
    return new_board
