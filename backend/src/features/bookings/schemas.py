from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime


class BookingBase(BaseModel):
    passenger_name: str
    passenger_age: int
    has_pet: bool = False
    flight_id: int

    @field_validator("passenger_age")
    @classmethod
    def age_must_be_valid(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("passenger_age debe estar entre 0 y 150")
        return v


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    total_price: float
    created_at: datetime
