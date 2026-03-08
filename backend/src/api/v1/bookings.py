from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from src.shared.database import get_db
from src.features.bookings import commands, queries, schemas

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/events")
async def get_booking_events(
    limit: int = 50,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Lista los eventos de reservas."""
    from src.features.bookings.event_log import BookingEvent

    query = db.query(BookingEvent).order_by(BookingEvent.created_at.desc())
    if event_type:
        query = query.filter(BookingEvent.event_type == event_type)
    events = query.limit(limit).all()
    return {
        "total": db.query(BookingEvent).count(),
        "events": [
            {
                "id": e.id,
                "event_type": e.event_type,
                "booking_id": e.booking_id,
                "payload": e.payload,
                "created_at": str(e.created_at),
            }
            for e in events
        ],
    }


@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return commands.create_booking(db=db, booking=booking)


@router.get("/", response_model=list[schemas.Booking])
def list_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return queries.get_bookings(db, skip=skip, limit=limit)
