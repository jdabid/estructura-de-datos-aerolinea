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


def get_demand_predictions() -> dict:
    """Obtiene predicciones de demanda para todos los destinos."""
    destinations = []
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match="stats:destination:*", count=100)
        for key in keys:
            dest_name = key.split(":")[-1]
            count = int(float(redis_client.get(key) or 0))
            destinations.append({"destination": dest_name, "current_bookings": count})
        if cursor == 0:
            break

    total_bookings = sum(d["current_bookings"] for d in destinations) if destinations else 0
    avg_bookings = total_bookings / len(destinations) if destinations else 0

    predictions = []
    for dest in destinations:
        count = dest["current_bookings"]
        market_share = (count / total_bookings * 100) if total_bookings > 0 else 0
        trend = "alta" if count > avg_bookings * 1.2 else "baja" if count < avg_bookings * 0.8 else "estable"
        projected = int(count * 1.1) if trend == "alta" else int(count * 0.9) if trend == "baja" else count

        predictions.append({
            "destination": dest["destination"],
            "current_bookings": count,
            "market_share_percent": round(market_share, 2),
            "trend": trend,
            "projected_next_period": projected,
        })

    predictions.sort(key=lambda x: x["current_bookings"], reverse=True)
    return {"predictions": predictions, "total_bookings": total_bookings}


def get_candy_logs() -> dict:
    """Obtiene los logs de distribucion de dulces."""
    entries = redis_client.lrange("logs:candy_distribution", 0, -1)
    return {
        "entries": entries,
        "total_count": len(entries),
    }
