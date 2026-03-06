from fastapi import FastAPI
from src.api.v1 import flights, bookings, ai

# Las tablas se gestionan con Alembic (ver alembic/ para migraciones)
# Para aplicar: alembic upgrade head

app = FastAPI(title="Flight Reservation System")

app.include_router(flights.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Sistema con Agente de IA Operativo"}