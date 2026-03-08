from sqlalchemy.orm import Session
from . import models, schemas
from src.worker.tasks import send_promotion_alert
import json
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

    if db_dest.is_promotion:
        try:
            promotion_payload = {
                "name": db_dest.name,
                "tax_amount": float(db_dest.tax_amount),
                "is_promotion": db_dest.is_promotion,
            }
            send_promotion_alert.delay(json.dumps(promotion_payload))
        except Exception:
            logger.exception("Failed to dispatch promotion alert for destination %s", db_dest.id)

    return db_dest


def create_flight(db: Session, flight: schemas.FlightCreate):
    db_flight = models.Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight
