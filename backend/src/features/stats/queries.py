from src.shared.redis_client import redis_client
from sqlalchemy.orm import Session
from src.features.flights.models import Destination


def get_general_stats() -> dict:
    """Obtiene estadisticas generales desde Redis."""
    return {
        "total_revenue": float(redis_client.get("stats:total_revenue") or 0),
        "total_pet_bookings": int(float(redis_client.get("stats:total_pet_bookings") or 0)),
        "total_infant_count": int(float(redis_client.get("stats:total_infant_count") or 0)),
        "total_candy_cost": float(redis_client.get("stats:total_candy_cost") or 0),
    }


def get_popular_destinations() -> dict:
    """Obtiene destinos por popularidad desde Redis."""
    destinations = []
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match="stats:destination:*", count=100)
        for key in keys:
            dest_name = key.split(":")[-1]
            count = int(float(redis_client.get(key) or 0))
            destinations.append({"destination": dest_name, "total_bookings": count})
        if cursor == 0:
            break

    destinations.sort(key=lambda x: x["total_bookings"], reverse=True)
    most_popular = destinations[0]["destination"] if destinations else None

    return {"destinations": destinations, "most_popular": most_popular}


def get_destination_tax_report(db: Session, destination_name: str) -> dict:
    """Obtiene reporte de impuestos para un destino especifico."""
    dest = db.query(Destination).filter(
        Destination.name.ilike(destination_name)
    ).first()

    if not dest:
        return None

    bookings_count = int(float(
        redis_client.get(f"stats:destination:{dest.name}") or 0
    ))

    return {
        "destination": dest.name,
        "tax_amount": dest.tax_amount,
        "total_bookings": bookings_count,
        "total_tax_collected": dest.tax_amount * bookings_count,
    }


def get_candy_logs() -> dict:
    """Obtiene los logs de distribucion de dulces."""
    entries = redis_client.lrange("logs:candy_distribution", 0, -1)
    return {
        "entries": entries,
        "total_count": len(entries),
    }
