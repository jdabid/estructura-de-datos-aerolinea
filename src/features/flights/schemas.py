from pydantic import BaseModel, ConfigDict, field_validator


class DestinationBase(BaseModel):
    name: str
    tax_amount: float
    is_promotion: bool = False
    allows_pets: bool = True

    @field_validator("tax_amount")
    @classmethod
    def tax_must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("tax_amount no puede ser negativo")
        return v


class DestinationCreate(DestinationBase):
    pass


class Destination(DestinationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FlightBase(BaseModel):
    flight_number: str
    origin: str
    base_price: float
    destination_id: int

    @field_validator("base_price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("base_price debe ser mayor a 0")
        return v


class FlightCreate(FlightBase):
    pass


class Flight(FlightBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    destination: Destination
