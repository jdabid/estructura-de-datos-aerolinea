from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.shared.database import get_db
from src.features.flights import commands, queries, schemas

router = APIRouter(prefix="/flights", tags=["flights"])

@router.post("/destinations/", response_model=schemas.Destination)
def create_destination(dest: schemas.DestinationCreate, db: Session = Depends(get_db)):
    return commands.create_destination(db=db, destination=dest)

@router.get("/destinations/", response_model=list[schemas.Destination])
def list_destinations(db: Session = Depends(get_db)):
    return queries.get_destinations(db)

@router.post("/", response_model=schemas.Flight)
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    return commands.create_flight(db=db, flight=flight)

@router.get("/", response_model=list[schemas.Flight])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return queries.get_flights(db, skip=skip, limit=limit)