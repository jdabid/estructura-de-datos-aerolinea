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


@tool
def search_destinations_by_description(query: str) -> str:
    """Busca destinos similares basandose en la descripcion usando busqueda semantica con pgvector."""
    from src.shared.embeddings import search_similar_destinations
    results = search_similar_destinations(query, limit=5)
    if not results:
        return "No se encontraron destinos con embeddings almacenados. Usa /ai/embed-destination primero."
    return json.dumps(results, ensure_ascii=False)


@tool
def predict_demand(destination_name: str) -> str:
    """Predice la demanda futura de un destino basandose en datos historicos de Redis y tendencias."""
    current_count = redis_client.get(f"stats:destination:{destination_name}") or 0
    current_count = int(current_count)

    all_stats = {}
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match="stats:destination:*", count=100)
        for key in keys:
            dest = key.split(":")[-1]
            all_stats[dest] = int(redis_client.get(key) or 0)
        if cursor == 0:
            break

    total_bookings = sum(all_stats.values()) if all_stats else 0
    market_share = (current_count / total_bookings * 100) if total_bookings > 0 else 0

    avg_bookings = total_bookings / len(all_stats) if all_stats else 0
    trend = "alta" if current_count > avg_bookings * 1.2 else "baja" if current_count < avg_bookings * 0.8 else "estable"

    projected_next_period = int(current_count * 1.1) if trend == "alta" else int(current_count * 0.9) if trend == "baja" else current_count

    return json.dumps({
        "destination": destination_name,
        "current_bookings": current_count,
        "market_share_percent": round(market_share, 2),
        "trend": trend,
        "projected_next_period": projected_next_period,
        "recommendation": f"Demanda {trend}. {'Considerar aumentar precios o capacidad.' if trend == 'alta' else 'Considerar promociones para estimular demanda.' if trend == 'baja' else 'Mantener estrategia actual.'}"
    }, ensure_ascii=False)
