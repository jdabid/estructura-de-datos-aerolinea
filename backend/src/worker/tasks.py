from .celery_app import celery_app
from src.shared.redis_client import update_stat, log_to_list
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@celery_app.task(name="handle_dead_letter", bind=True)
def handle_dead_letter(self, original_task_name: str, original_args: str, error_message: str):
    """Procesa mensajes que fallaron despues de todos los reintentos."""
    log_to_list(
        "logs:dead_letter",
        json.dumps({
            "task": original_task_name,
            "args": original_args,
            "error": error_message,
            "timestamp": str(datetime.utcnow()),
        }),
    )
    update_stat("stats:dead_letter_count", 1)
    logger.error(f"Dead letter: {original_task_name} - {error_message}")
    return f"Dead letter registrada para {original_task_name}"


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
        if self.request.retries >= self.max_retries:
            handle_dead_letter.delay(
                "process_booking_event",
                booking_data,
                str(exc),
            )
            return f"Reserva enviada a dead letter queue tras {self.max_retries} reintentos"
        raise self.retry(exc=exc)
