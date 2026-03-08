from sqlalchemy.orm import Session
from . import models, schemas
import logging

logger = logging.getLogger(__name__)


def create_destination(db: Session, destination: schemas.DestinationCreate):
    db_dest = models.Destination(**destination.model_dump())
    db.add(db_dest)
    db.commit()
    db.refresh(db_dest)

    # Auto-generar embedding para busqueda semantica
    try:
        from src.shared.embeddings import store_destination_embedding
        description = db_dest.name
        store_destination_embedding(db_dest.id, description)
    except Exception:
        logger.warning("No se pudo generar embedding para destino %s", db_dest.id)

    return db_dest


def create_flight(db: Session, flight: schemas.FlightCreate):
    db_flight = models.Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight
