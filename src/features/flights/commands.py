from sqlalchemy.orm import Session
from . import models, schemas


def create_destination(db: Session, destination: schemas.DestinationCreate):
    db_dest = models.Destination(**destination.model_dump())
    db.add(db_dest)
    db.commit()
    db.refresh(db_dest)
    return db_dest


def create_flight(db: Session, flight: schemas.FlightCreate):
    db_flight = models.Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight
