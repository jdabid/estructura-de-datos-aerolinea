from langchain.tools import tool
from src.shared.database import SessionLocal
from src.features.flights.models import Flight, Destination
from src.shared.redis_client import redis_client
import json


@tool
def get_flight_market_data(destination_name: str) -> str:
    """Consulta el precio base, impuestos y si tiene promoción un destino específico."""
    db = SessionLocal()
    try:
        dest = db.query(Destination).filter(
            Destination.name.ilike(destination_name)
        ).first()
        if not dest:
            return f"No se encontró información para el destino {destination_name}."

        flights = db.query(Flight).filter(Flight.destination_id == dest.id).all()
        prices = [f.base_price for f in flights]
        avg_price = sum(prices) / len(prices) if prices else 0

        return json.dumps({
            "destination": dest.name,
            "tax": dest.tax_amount,
            "is_promotion": dest.is_promotion,
            "average_base_price": avg_price,
            "allows_pets": dest.allows_pets,
        })
    finally:
        db.close()


@tool
def get_demand_stats() -> str:
    """Obtiene estadísticas de demanda y popularidad desde Redis."""
    stats = {}
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match="stats:destination:*", count=100)
        for key in keys:
            dest_name = key.split(":")[-1]
            stats[dest_name] = redis_client.get(key)
        if cursor == 0:
            break

    total_revenue = redis_client.get("stats:total_revenue") or 0
    total_infant_count = redis_client.get("stats:total_infant_count") or 0

    return json.dumps({
        "popular_destinations": stats,
        "total_revenue_to_date": total_revenue,
        "total_infant_travelers": total_infant_count,
    })
