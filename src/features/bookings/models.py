from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.shared.database import Base
import datetime


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    passenger_name = Column(String)
    passenger_age = Column(Integer)
    has_pet = Column(Boolean, default=False)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    flight_id = Column(Integer, ForeignKey("flights.id"))