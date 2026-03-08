from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.shared.database import get_db
from src.features.stats import schemas, queries

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/general", response_model=schemas.GeneralStats)
def get_general_stats():
    """Estadisticas generales: recaudo total, mascotas, infantes, dulces."""
    return queries.get_general_stats()


@router.get("/destinations", response_model=schemas.PopularDestinations)
def get_popular_destinations():
    """Destinos por popularidad con el mas preferido."""
    return queries.get_popular_destinations()


@router.get("/destinations/{destination_name}/taxes", response_model=schemas.DestinationTaxReport)
def get_destination_taxes(destination_name: str, db: Session = Depends(get_db)):
    """Total de impuestos recaudados para un destino especifico."""
    result = queries.get_destination_tax_report(db, destination_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Destino '{destination_name}' no encontrado")
    return result


@router.get("/candy", response_model=schemas.CandyLog)
def get_candy_distribution():
    """Logs de distribucion de dulces a infantes."""
    return queries.get_candy_logs()


@router.get("/dead-letters")
async def get_dead_letters(limit: int = 20):
    """Lista los ultimos mensajes en la dead letter queue."""
    from src.shared.redis_client import redis_client
    import json
    entries = redis_client.lrange("logs:dead_letter", 0, limit - 1)
    return {
        "count": redis_client.llen("logs:dead_letter"),
        "entries": [json.loads(e) for e in entries],
    }


@router.get("/notifications")
async def get_notifications(limit: int = 20):
    """Lista las ultimas notificaciones enviadas."""
    from src.shared.redis_client import redis_client
    import json
    entries = redis_client.lrange("logs:notifications", 0, limit - 1)
    return {
        "total_sent": int(redis_client.get("stats:notifications_sent") or 0),
        "notifications": [json.loads(e) for e in entries],
    }
