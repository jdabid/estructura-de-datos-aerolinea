from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.shared.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    passenger_name = Column(String, nullable=False)
    passenger_age = Column(Integer, nullable=False)
    has_pet = Column(Boolean, default=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    flight = relationship("Flight", back_populates="bookings")