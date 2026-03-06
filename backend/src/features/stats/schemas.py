from pydantic import BaseModel


class GeneralStats(BaseModel):
    total_revenue: float
    total_pet_bookings: int
    total_infant_count: int
    total_candy_cost: float


class DestinationStats(BaseModel):
    destination: str
    total_bookings: int


class DestinationTaxReport(BaseModel):
    destination: str
    tax_amount: float
    total_bookings: int
    total_tax_collected: float


class CandyLog(BaseModel):
    entries: list[str]
    total_count: int


class PopularDestinations(BaseModel):
    destinations: list[DestinationStats]
    most_popular: str | None
