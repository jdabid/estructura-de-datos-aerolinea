from sqlalchemy.orm import Session
from . import models, schemas
from src.features.flights.models import Flight
from src.shared.exceptions import NotFoundException, ValidationException
from src.worker.tasks import process_booking_event, send_booking_confirmation
from src.features.bookings.event_logger import log_booking_event
from src.shared.metrics import BOOKINGS_TOTAL, BOOKING_PRICE
import json
import logging

logger = logging.getLogger(__name__)


def create_booking(db: Session, booking: schemas.BookingCreate):
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if not flight:
        raise NotFoundException("El vuelo seleccionado no existe.")

    destination = flight.destination
    if booking.has_pet and not destination.allows_pets:
        raise ValidationException(f"El destino {destination.name} no acepta mascotas.")

    price = flight.base_price
    if destination.is_promotion:
        price *= 0.90

    total_final = price + destination.tax_amount

    db_booking = models.Booking(
        passenger_name=booking.passenger_name,
        passenger_age=booking.passenger_age,
        has_pet=booking.has_pet,
        flight_id=booking.flight_id,
        total_price=total_final,
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    BOOKINGS_TOTAL.labels(destination=destination.name).inc()
    BOOKING_PRICE.observe(total_final)

    payload = {
        "id": db_booking.id,
        "passenger_name": db_booking.passenger_name,
        "passenger_age": db_booking.passenger_age,
        "has_pet": db_booking.has_pet,
        "total_price": float(db_booking.total_price),
        "destination_name": destination.name,
    }

    try:
        process_booking_event.delay(json.dumps(payload))
    except Exception:
        logger.exception("Failed to dispatch booking event for booking %s", db_booking.id)

    try:
        confirmation_payload = {
            "id": db_booking.id,
            "passenger_name": db_booking.passenger_name,
            "flight_number": flight.flight_number,
            "total_price": float(db_booking.total_price),
        }
        send_booking_confirmation.delay(json.dumps(confirmation_payload))
    except Exception:
        logger.exception("Failed to dispatch booking confirmation for booking %s", db_booking.id)

    log_booking_event("booking_created", db_booking.id, payload)

    return db_booking
