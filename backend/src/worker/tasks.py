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


@celery_app.task(name="send_booking_confirmation", bind=True, max_retries=3, default_retry_delay=5)
def send_booking_confirmation(self, booking_data: str):
    """Simula envio de confirmacion de reserva por email."""
    try:
        data = json.loads(booking_data)
        confirmation = {
            "type": "booking_confirmation",
            "passenger": data["passenger_name"],
            "flight": data.get("flight_number", "N/A"),
            "total": data["total_price"],
            "timestamp": str(datetime.utcnow()),
        }
        log_to_list("logs:notifications", json.dumps(confirmation))
        update_stat("stats:notifications_sent", 1)
        logger.info(f"Confirmacion enviada a {data['passenger_name']}")
        return f"Confirmacion enviada para reserva {data['id']}"
    except Exception as exc:
        logger.exception("Error sending booking confirmation")
        raise self.retry(exc=exc)


@celery_app.task(name="send_promotion_alert", bind=True, max_retries=3, default_retry_delay=5)
def send_promotion_alert(self, destination_data: str):
    """Notifica cuando un destino entra en promocion."""
    try:
        data = json.loads(destination_data)
        alert = {
            "type": "promotion_alert",
            "destination": data["name"],
            "discount": "10%",
            "timestamp": str(datetime.utcnow()),
        }
        log_to_list("logs:notifications", json.dumps(alert))
        update_stat("stats:promotion_alerts_sent", 1)
        logger.info(f"Alerta de promocion para {data['name']}")
        return f"Alerta de promocion enviada para {data['name']}"
    except Exception as exc:
        logger.exception("Error sending promotion alert")
        raise self.retry(exc=exc)


@celery_app.task(name="send_pet_rejection_notice", bind=True, max_retries=2, default_retry_delay=5)
def send_pet_rejection_notice(self, passenger_name: str, destination_name: str):
    """Notifica cuando una reserva con mascota es rechazada."""
    try:
        notice = {
            "type": "pet_rejection",
            "passenger": passenger_name,
            "destination": destination_name,
            "reason": "El destino no permite mascotas",
            "timestamp": str(datetime.utcnow()),
        }
        log_to_list("logs:notifications", json.dumps(notice))
        update_stat("stats:pet_rejections_notified", 1)
        logger.info(f"Notificacion de rechazo de mascota para {passenger_name}")
        return f"Notificacion de rechazo enviada a {passenger_name}"
    except Exception as exc:
        logger.exception("Error sending pet rejection notice")
        raise self.retry(exc=exc)
