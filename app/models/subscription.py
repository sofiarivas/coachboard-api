from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (UniqueConstraint("trainee_id", "board_id", name="uq_trainee_board"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    trainee_id = Column(UUID(as_uuid=True), ForeignKey("trainees.id", ondelete="CASCADE"), nullable=False)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    trainee = relationship("Trainee", back_populates="subscriptions")
    board = relationship("Board", back_populates="subscriptions")
