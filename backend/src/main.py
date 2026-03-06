from fastapi import FastAPI
from src.api.v1 import flights, bookings, ai
from src.shared.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Reservation System - Week 5 (AI Ready)")

# Registro de Rutas
app.include_router(flights.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Sistema con Agente de IA Operativo"}