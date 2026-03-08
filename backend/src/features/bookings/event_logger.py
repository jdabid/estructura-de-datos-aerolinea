from src.shared.database import SessionLocal
from src.features.bookings.event_log import BookingEvent
from src.shared.redis_client import log_to_list
import json
import logging

logger = logging.getLogger(__name__)


def log_booking_event(event_type: str, booking_id: int | None, payload: dict) -> None:
    """Registra un evento de reserva en PostgreSQL y Redis."""
    db = SessionLocal()
    try:
        event = BookingEvent(
            event_type=event_type,
            booking_id=booking_id,
            payload=payload,
        )
        db.add(event)
        db.commit()

        # Also log to Redis for real-time access
        log_to_list("logs:booking_events", json.dumps({
            "event_type": event_type,
            "booking_id": booking_id,
            "payload": payload,
        }))
        logger.info(f"Event logged: {event_type} for booking {booking_id}")
    except Exception:
        db.rollback()
        logger.exception(f"Failed to log event: {event_type}")
    finally:
        db.close()
