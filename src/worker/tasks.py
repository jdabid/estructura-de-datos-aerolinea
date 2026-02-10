from .celery_app import celery_app
from src.shared.redis_client import update_stat, log_to_list
import json


@celery_app.task(name="process_booking_event")
def process_booking_event(booking_data: str):
    data = json.loads(booking_data)

    # 1. Actualizar Estadística de Recaudo Total en Redis
    update_stat("stats:total_revenue", data["total_price"])

    # 2. Actualizar Popularidad del Destino
    dest_key = f"stats:destination:{data['destination_name']}"
    update_stat(dest_key, 1)

    # 3. Lógica de Dulces para Infantes
    if data["passenger_age"] < 12:
        candy_cost = 5.0  # Costo fijo por dulce
        update_stat("stats:total_candy_cost", candy_cost)
        log_to_list("logs:candy_distribution", f"Reserva {data['id']}: Dulce entregado a {data['passenger_name']}")

    return f"Procesada reserva {data['id']} exitosamente"