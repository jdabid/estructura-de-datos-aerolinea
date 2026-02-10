from pydantic import BaseModel
from typing import List, Optional

class DestinationBase(BaseModel):
    name: str
    tax_amount: float
    is_promotion: bool = False

class DestinationCreate(DestinationBase):
    pass

class Destination(DestinationBase):
    id: int
    class Config:
        orm_mode = True

class FlightBase(BaseModel):
    flight_number: str
    origin: str
    base_price: float
    destination_id: int

class FlightCreate(FlightBase):
    pass

class Flight(FlightBase):
    id: int
    destination: Destination
    class Config:
        orm_mode = True