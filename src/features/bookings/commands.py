from sqlalchemy.orm import Session
from . import models, schemas
from src.features.flights.models import Flight


def create_booking(db: Session, booking: schemas.BookingCreate):
    # 1. Obtener información del vuelo y destino
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    if not flight:
        raise ValueError("El vuelo seleccionado no existe.")

    destination = flight.destination

    # 2. Validación de Mascotas
    if booking.has_pet and not destination.allows_pets:
        raise ValueError(f"El destino {destination.name} no acepta mascotas.")

    # 3. Cálculo de Precio con Reglas de Negocio
    price = flight.base_price

    # Aplicar 10% de descuento si es promoción
    if destination.is_promotion:
        price = price * 0.90

    # Sumar impuestos del destino
    total_final = price + destination.tax_amount

    # 4. Persistencia
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

    # Nota: En la Semana 4 integraremos aquí el disparo del evento para los dulces de infantes.
    return db_booking