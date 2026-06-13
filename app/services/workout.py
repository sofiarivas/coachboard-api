from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models import Workout, Subscription
from datetime import datetime, date

async def get_today_workouts(session: AsyncSession, trainee_id):
    today = date.today()
    result = await session.execute(
        select(Workout)
        .join(Subscription, Subscription.board_id == Workout.board_id)
        .where(
            and_(
                Subscription.trainee_id == trainee_id,
                Workout.status == "published",
                Workout.scheduled_at >= datetime.combine(today, datetime.min.time()),
                Workout.scheduled_at < datetime.combine(date.fromordinal(today.toordinal() + 1), datetime.min.time())
            )
        )
        .order_by(Workout.scheduled_at)
    )
    return result.scalars().all()

async def get_upcoming_workouts(session: AsyncSession, trainee_id, days: int = 7):
    today = date.today()
    result = await session.execute(
        select(Workout)
        .join(Subscription, Subscription.board_id == Workout.board_id)
        .where(
            and_(
                Subscription.trainee_id == trainee_id,
                Workout.status == "published",
                Workout.scheduled_at >= datetime.combine(today, datetime.min.time())
            )
        )
        .order_by(Workout.scheduled_at)
        .limit(days * 10)
    )
    return result.scalars().all()
