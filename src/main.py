from fastapi import FastAPI
from src.api.v1 import flights
from src.shared.database import engine, Base

# Crear tablas en la DB (Simplicidad para MVP)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flight Reservation System - Week 2")

# Registrar Rutas
app.include_router(flights.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Gestión de Vuelos Operativa"}