from unittest.mock import patch, MagicMock
import pytest
from pydantic import ValidationError

from src.features.flights.models import Destination, Flight
from src.features.bookings.models import Booking
from src.features.bookings.schemas import BookingCreate
from src.features.bookings.commands import create_booking
from src.shared.exceptions import NotFoundException, ValidationException


def _create_destination(db, name="Cancun", tax_amount=50.0, is_promotion=False, allows_pets=True):
    dest = Destination(name=name, tax_amount=tax_amount, is_promotion=is_promotion, allows_pets=allows_pets)
    db.add(dest)
    db.commit()
    db.refresh(dest)
    return dest


def _create_flight(db, destination, flight_number="FL-100", origin="Bogota", base_price=200.0):
    flight = Flight(
        flight_number=flight_number,
        origin=origin,
        base_price=base_price,
        destination_id=destination.id,
    )
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return flight


@patch("src.features.bookings.commands.process_booking_event")
def test_create_booking_no_promo_no_pet(mock_task, db_session):
    """Reserva exitosa sin promocion ni mascota: precio = base_price + tax."""
    dest = _create_destination(db_session, tax_amount=50.0, is_promotion=False)
    flight = _create_flight(db_session, dest, base_price=200.0)

    booking_data = BookingCreate(
        passenger_name="Juan Perez",
        passenger_age=30,
        has_pet=False,
        flight_id=flight.id,
    )
    result = create_booking(db_session, booking_data)

    assert result.total_price == 250.0  # 200 + 50
    assert result.passenger_name == "Juan Perez"
    assert result.flight_id == flight.id
    mock_task.delay.assert_called_once()


@patch("src.features.bookings.commands.process_booking_event")
def test_create_booking_with_promotion(mock_task, db_session):
    """Reserva con promocion: precio = base_price * 0.90 + tax."""
    dest = _create_destination(db_session, tax_amount=30.0, is_promotion=True)
    flight = _create_flight(db_session, dest, base_price=100.0)

    booking_data = BookingCreate(
        passenger_name="Maria Lopez",
        passenger_age=25,
        has_pet=False,
        flight_id=flight.id,
    )
    result = create_booking(db_session, booking_data)

    expected_price = 100.0 * 0.90 + 30.0  # 90 + 30 = 120
    assert result.total_price == pytest.approx(expected_price)


@patch("src.features.bookings.commands.process_booking_event")
def test_create_booking_pet_allowed(mock_task, db_session):
    """Reserva con mascota en destino que permite mascotas: exitosa."""
    dest = _create_destination(db_session, allows_pets=True)
    flight = _create_flight(db_session, dest)

    booking_data = BookingCreate(
        passenger_name="Carlos Ruiz",
        passenger_age=40,
        has_pet=True,
        flight_id=flight.id,
    )
    result = create_booking(db_session, booking_data)

    assert result.has_pet is True
    assert result.id is not None


@patch("src.features.bookings.commands.process_booking_event")
def test_create_booking_pet_not_allowed(mock_task, db_session):
    """Reserva con mascota en destino que NO permite mascotas: ValidationException."""
    dest = _create_destination(db_session, name="Tokyo", allows_pets=False)
    flight = _create_flight(db_session, dest)

    booking_data = BookingCreate(
        passenger_name="Ana Torres",
        passenger_age=28,
        has_pet=True,
        flight_id=flight.id,
    )

    with pytest.raises(ValidationException) as exc_info:
        create_booking(db_session, booking_data)

    assert "Tokyo" in exc_info.value.detail
    assert "mascotas" in exc_info.value.detail


@patch("src.features.bookings.commands.process_booking_event")
def test_create_booking_flight_not_found(mock_task, db_session):
    """Reserva con vuelo inexistente: NotFoundException."""
    booking_data = BookingCreate(
        passenger_name="Pedro Garcia",
        passenger_age=35,
        has_pet=False,
        flight_id=9999,
    )

    with pytest.raises(NotFoundException) as exc_info:
        create_booking(db_session, booking_data)

    assert "vuelo" in exc_info.value.detail.lower()


@patch("src.features.bookings.commands.process_booking_event")
def test_create_booking_celery_failure_does_not_break(mock_task, db_session):
    """Si Celery falla, la reserva se crea igual (el error se loguea)."""
    mock_task.delay.side_effect = Exception("RabbitMQ down")
    dest = _create_destination(db_session)
    flight = _create_flight(db_session, dest)

    booking_data = BookingCreate(
        passenger_name="Luis Mendez",
        passenger_age=22,
        has_pet=False,
        flight_id=flight.id,
    )

    result = create_booking(db_session, booking_data)

    assert result.id is not None
    assert result.passenger_name == "Luis Mendez"


def test_schema_age_negative():
    """Edad negativa lanza ValidationError."""
    with pytest.raises(ValidationError):
        BookingCreate(
            passenger_name="Test",
            passenger_age=-1,
            has_pet=False,
            flight_id=1,
        )


def test_schema_age_exceeds_max():
    """Edad mayor a 150 lanza ValidationError."""
    with pytest.raises(ValidationError):
        BookingCreate(
            passenger_name="Test",
            passenger_age=151,
            has_pet=False,
            flight_id=1,
        )
