from sqlalchemy.orm import Session
from . import models, schemas
from src.features.flights.models import Flight
from src.worker.tasks import process_booking_event
import json


def create_booking(db: Session, booking: schemas.BookingCreate):
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if not flight:
        raise ValueError("El vuelo seleccionado no existe.")

    destination = flight.destination

    if booking.has_pet and not destination.allows_pets:
        raise ValueError(f"El destino {destination.name} no acepta mascotas.")

    price = flight.base_price
    if destination.is_promotion:
        price = price * 0.90

    total_final = price + destination.tax_amount

    db_booking = models.Booking(
        passenger_name=booking.passenger_name,
        passenger_age=booking.passenger_age,
        has_pet=booking.has_pet,
        flight_id=booking.flight_id,
        total_price=total_final
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # --- SEMANA 4: DISPARO DE EVENTO ASÍNCRONO ---
    payload = {
        "id": db_booking.id,
        "passenger_name": db_booking.passenger_name,
        "passenger_age": db_booking.passenger_age,
        "total_price": db_booking.total_price,
        "destination_name": destination.name
    }
    process_booking_event.delay(json.dumps(payload))
    # ---------------------------------------------

    return db_booking