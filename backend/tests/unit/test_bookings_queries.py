from src.features.flights.models import Destination, Flight
from src.features.bookings.models import Booking
from src.features.bookings.queries import get_bookings, get_booking_by_id


def _seed_booking(db, passenger_name="Test User", passenger_age=30, has_pet=False):
    dest = Destination(name=f"Dest-{passenger_name}", tax_amount=10.0, is_promotion=False, allows_pets=True)
    db.add(dest)
    db.commit()
    db.refresh(dest)

    flight = Flight(flight_number=f"FL-{passenger_name}", origin="Bogota", base_price=100.0, destination_id=dest.id)
    db.add(flight)
    db.commit()
    db.refresh(flight)

    booking = Booking(
        passenger_name=passenger_name,
        passenger_age=passenger_age,
        has_pet=has_pet,
        total_price=110.0,
        flight_id=flight.id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def test_get_bookings_empty(db_session):
    """Sin reservas, retorna lista vacia."""
    result = get_bookings(db_session)
    assert result == []


def test_get_bookings_returns_all(db_session):
    """Retorna todas las reservas existentes."""
    _seed_booking(db_session, passenger_name="Alice")
    _seed_booking(db_session, passenger_name="Bob")

    result = get_bookings(db_session)
    assert len(result) == 2
    names = {b.passenger_name for b in result}
    assert names == {"Alice", "Bob"}


def test_get_booking_by_id_found(db_session):
    """Retorna la reserva correcta por ID."""
    booking = _seed_booking(db_session, passenger_name="Carlos")
    result = get_booking_by_id(db_session, booking.id)
    assert result is not None
    assert result.passenger_name == "Carlos"


def test_get_booking_by_id_not_found(db_session):
    """Retorna None si no existe la reserva."""
    result = get_booking_by_id(db_session, 9999)
    assert result is None
