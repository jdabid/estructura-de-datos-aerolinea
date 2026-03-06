from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import flights, bookings, ai, auth
from src.shared.exceptions import AppException, app_exception_handler
from src.shared.middleware import RateLimitMiddleware

# Las tablas se gestionan con Alembic (ver alembic/ para migraciones)
# Para aplicar: alembic upgrade head

app = FastAPI(title="Flight Reservation System")

app.add_exception_handler(AppException, app_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting: 60 requests por minuto por IP
app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

app.include_router(flights.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Sistema con Agente de IA Operativo"}
