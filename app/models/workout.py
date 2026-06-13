from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.database import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="draft")
    content = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    board = relationship("Board", back_populates="workouts")
