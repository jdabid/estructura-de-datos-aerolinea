from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    passenger_name: str
    passenger_age: int
    has_pet: bool = False
    flight_id: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True