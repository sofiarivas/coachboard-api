from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.database import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coaches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    visibility = Column(String, default="public")
    created_at = Column(DateTime, server_default=func.now())

    coach = relationship("Coach", back_populates="boards")
    workouts = relationship("Workout", back_populates="board", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="board", cascade="all, delete-orphan")
