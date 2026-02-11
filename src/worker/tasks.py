from .celery_app import celery_app
from src.shared.redis_client import update_stat, log_to_list
import json
import logging

logger = logging.getLogger(__name__)


@celery_app.task(
    name="process_booking_event",
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def process_booking_event(self, booking_data: str):
    try:
        data = json.loads(booking_data)

        update_stat("stats:total_revenue", data["total_price"])

        dest_key = f"stats:destination:{data['destination_name']}"
        update_stat(dest_key, 1)

        if data.get("has_pet"):
            update_stat("stats:total_pet_bookings", 1)

        if data["passenger_age"] < 12:
            candy_cost = 5.0
            update_stat("stats:total_candy_cost", candy_cost)
            update_stat("stats:total_infant_count", 1)
            log_to_list(
                "logs:candy_distribution",
                f"Reserva {data['id']}: Dulce entregado a {data['passenger_name']}",
            )

        return f"Procesada reserva {data['id']} exitosamente"
    except Exception as exc:
        logger.exception("Error processing booking event")
        raise self.retry(exc=exc)
