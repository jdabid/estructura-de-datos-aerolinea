from sqlalchemy.orm import Session
from . import models


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_destinations(db: Session):
    return db.query(models.Destination).all()


def get_flight_by_number(db: Session, flight_number: str):
    return db.query(models.Flight).filter(
        models.Flight.flight_number == flight_number
    ).first()
