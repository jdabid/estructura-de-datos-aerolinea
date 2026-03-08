from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from src.shared.database import Base


class BookingEvent(Base):
    __tablename__ = "booking_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, index=True)
    booking_id = Column(Integer, nullable=True)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
