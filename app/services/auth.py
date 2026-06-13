from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Coach, Trainee
from app.utils.security import hash_password, verify_password
from datetime import timedelta

async def register_coach(session: AsyncSession, name: str, email: str, password: str, bio: str = None, avatar_url: str = None):
    coach = Coach(name=name, email=email, password_hash=hash_password(password), bio=bio, avatar_url=avatar_url)
    session.add(coach)
    await session.commit()
    await session.refresh(coach)
    return coach

async def login_coach(session: AsyncSession, email: str, password: str):
    result = await session.execute(select(Coach).where(Coach.email == email))
    coach = result.scalar_one_or_none()
    if not coach or not verify_password(password, coach.password_hash):
        return None
    return coach

async def register_trainee(session: AsyncSession, name: str, email: str, password: str):
    trainee = Trainee(name=name, email=email, password_hash=hash_password(password))
    session.add(trainee)
    await session.commit()
    await session.refresh(trainee)
    return trainee

async def login_trainee(session: AsyncSession, email: str, password: str):
    result = await session.execute(select(Trainee).where(Trainee.email == email))
    trainee = result.scalar_one_or_none()
    if not trainee or not verify_password(password, trainee.password_hash):
        return None
    return trainee
