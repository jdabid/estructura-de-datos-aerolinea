# Flight Reservation System

Sistema de reserva de vuelos con arquitectura moderna, procesamiento asincrono y agente de IA.

## Stack Tecnologico

| Capa | Tecnologia |
|------|------------|
| API | Python 3.11, FastAPI, Pydantic v2 |
| Base de datos | PostgreSQL 15 (volumen persistente) |
| Cache / Stats | Redis 7 |
| Message Broker | RabbitMQ 3 |
| Worker | Celery 5 |
| AI Agent | LangChain + Groq (Llama 3.3 70B) - Patron RAG |
| Contenedores | Docker (multi-stage build, usuario no-root) |
| Orquestacion | Kubernetes + Helm Charts (HPA) |
| CI/CD | GitHub Actions + ghcr.io |

## Arquitectura

**Vertical Slice Architecture + CQRS**

```
src/
├── main.py                          # FastAPI app entry point
├── api/v1/
│   ├── flights.py                   # Rutas de vuelos y destinos
│   ├── bookings.py                  # Rutas de reservas
│   └── ai.py                        # Rutas del agente de IA (patron RAG)
├── features/
│   ├── flights/
│   │   ├── models.py                # ORM: Destination, Flight
│   │   ├── schemas.py               # Schemas Pydantic v2
│   │   ├── commands.py              # Escritura: crear destino, crear vuelo
│   │   └── queries.py               # Lectura: listar vuelos
│   ├── bookings/
│   │   ├── models.py                # ORM: Booking
│   │   ├── schemas.py               # Schemas Pydantic v2
│   │   ├── commands.py              # Logica de negocio: precio, descuento, impuesto
│   │   └── queries.py               # Lectura: listar reservas
│   └── ai/
│       ├── agent.py                 # Singleton LLM (ChatGroq + lru_cache)
│       └── tools.py                 # Tools: market data (PostgreSQL), demand stats (Redis)
├── shared/
│   ├── database.py                  # SQLAlchemy 2.0 engine + SessionLocal
│   └── redis_client.py              # Cliente Redis (incrbyfloat, lpush, scan)
└── worker/
    ├── celery_app.py                # Configuracion Celery + RabbitMQ
    └── tasks.py                     # Task: process_booking_event (max_retries=3)

infra/
├── docker/Dockerfile                # Build multi-stage (usuario no-root: appuser)
└── helm/flight-app/templates/
    └── deployment.yaml              # Deployment + HPA (min 2 / max 10, CPU 70%)

tests/
└── test_integration.py              # 4 tests de integracion

.github/workflows/
└── deploy.yml                       # Pipeline CI/CD (ghcr.io + deploy condicional)
```

## Logica de Negocio

Al crear una reserva el sistema aplica:

1. **Descuento por promocion**: si el destino tiene `is_promotion: true` aplica 10% de descuento sobre `base_price`
2. **Impuesto por destino**: suma `tax_amount` del destino al precio
3. **Validacion de mascotas**: si `has_pet: true` y el destino no permite mascotas, rechaza con 400
4. **Validacion de edad**: `passenger_age` debe ser >= 0 (Pydantic `field_validator`)
5. **Validacion de precio**: `base_price` debe ser > 0 (Pydantic `field_validator`)
6. **Evento asincrono**: Celery publica en RabbitMQ y el worker actualiza Redis con recaudo total, popularidad por destino, dulces para infantes < 12 anios

**Formula:** `total_price = (base_price * 0.90 si promocion, o base_price) + tax_amount`

## Agente de IA - Patron RAG

El sistema implementa un agente de IA usando el patron **RAG (Retrieval-Augmented Generation)**:

1. **Recuperacion**: Los tools (`get_flight_market_data`, `get_demand_stats`) consultan datos reales de PostgreSQL y Redis
2. **Enriquecimiento**: El prompt se construye con los datos recuperados + la pregunta del usuario
3. **Generacion**: El LLM (Llama 3.3 70B via Groq) genera una respuesta basada en datos reales

```
Usuario → API → Tools (PostgreSQL/Redis) → Prompt enriquecido → LLM (Groq) → Respuesta
```

**Endpoints IA:**
- `POST /api/v1/ai/chat` - Chatbot general sobre vuelos
- `POST /api/v1/ai/suggest-price` - Analista de precios con recomendaciones concretas

---

## Requisitos Previos

- Docker y Docker Compose instalados
- GROQ_API_KEY valida (gratis en [console.groq.com](https://console.groq.com)) - solo para endpoints `/ai/*`

```bash
docker --version          # Docker 20+ requerido
docker compose version    # Compose v2+ requerido
```

---

## Paso a Paso: Ejecutar la Aplicacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/jdabid/flight-reservation-system.git
cd flight-reservation-system
```

### 2. Crear archivo `.env`

```bash
cat <<'EOF' > .env
GROQ_API_KEY=gsk-tu-clave-de-groq-aqui
EOF
```

> Las demas variables (DATABASE_URL, RABBITMQ_URL, REDIS_HOST) estan configuradas directamente en `docker-compose.yml`.

### 3. Levantar todos los servicios

```bash
docker compose up --build -d
```

Esto levanta 5 contenedores:

| Servicio | Puerto | Descripcion |
|----------|--------|-------------|
| api | 8000 | FastAPI (uvicorn) |
| worker | - | Celery worker |
| db | 5432 | PostgreSQL 15 (volumen persistente) |
| redis | 6379 | Redis 7 |
| rabbitmq | 5672 / 15672 | RabbitMQ + Management UI |

### 4. Verificar que todo esta corriendo

```bash
docker compose ps
```

Todos los servicios deben mostrar estado `Up (healthy)`.

### 5. Health check

```bash
curl http://localhost:8000/
```

Respuesta esperada:

```json
{"status": "ok", "message": "Sistema con Agente de IA Operativo"}
```

### 6. Documentacion interactiva

Abrir en el navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Paso a Paso: Probar el Flujo Completo

### Paso 1 - Crear un destino

```bash
curl -X POST http://localhost:8000/api/v1/flights/destinations/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cartagena",
    "tax_amount": 50.0,
    "is_promotion": true,
    "allows_pets": true
  }'
```

### Paso 2 - Crear un vuelo

```bash
curl -X POST http://localhost:8000/api/v1/flights/ \
  -H "Content-Type: application/json" \
  -d '{
    "flight_number": "CT-123",
    "origin": "Bogota",
    "base_price": 1000.0,
    "destination_id": 1
  }'
```

### Paso 3 - Crear una reserva (precio esperado: 950)

```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "passenger_name": "Juan Perez",
    "passenger_age": 30,
    "has_pet": true,
    "flight_id": 1
  }'
```

**Calculo:** `1000 * 0.90 + 50 = 950.0`

### Paso 4 - Verificar el worker

```bash
docker compose logs worker --tail 20
```

### Paso 5 - Consultar estadisticas en Redis

```bash
docker compose exec redis redis-cli GET stats:total_revenue
docker compose exec redis redis-cli GET stats:destination:Cartagena
docker compose exec redis redis-cli GET stats:total_candy_cost
docker compose exec redis redis-cli GET stats:total_infant_count
docker compose exec redis redis-cli GET stats:total_pet_bookings
```

### Paso 6 - Probar validacion de mascotas (debe dar error 400)

```bash
curl -X POST http://localhost:8000/api/v1/flights/destinations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Londres", "tax_amount": 100, "is_promotion": false, "allows_pets": false}'

curl -X POST http://localhost:8000/api/v1/flights/ \
  -H "Content-Type: application/json" \
  -d '{"flight_number": "LON-99", "origin": "Bogota", "base_price": 2000, "destination_id": 2}'

curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"passenger_name": "Test User", "passenger_age": 25, "has_pet": true, "flight_id": 2}'
```

Respuesta esperada:

```json
{"detail": "El destino Londres no acepta mascotas."}
```

### Paso 7 - Probar reserva de infante (dulce automatico)

```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"passenger_name": "Pedrito", "passenger_age": 8, "has_pet": false, "flight_id": 1}'
```

Verificar dulce en Redis:

```bash
docker compose exec redis redis-cli LRANGE logs:candy_distribution 0 -1
```

### Paso 8 - Probar el agente de IA (requiere GROQ_API_KEY)

```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Cuanto cuestan los impuestos para viajar a Cartagena?"}'

curl -X POST http://localhost:8000/api/v1/ai/suggest-price \
  -H "Content-Type: application/json" \
  -d '{"destination_name": "Cartagena"}'
```

---

## Ejecutar Tests

### Opcion A - Dentro de Docker (recomendado)

```bash
docker compose exec api pytest tests/ -v --tb=short
```

> Despues de ejecutar tests, reiniciar la API para recrear las tablas:
> ```bash
> docker compose restart api
> ```

### Opcion B - Local con la DB del compose

```bash
docker compose up db redis -d

pip install -r requirements.txt

DATABASE_URL=postgresql://user:pass@localhost:5432/flights \
REDIS_HOST=localhost \
RABBITMQ_URL="" \
pytest tests/ -v --tb=short
```

### Tests incluidos

| Test | Valida |
|------|--------|
| `test_full_booking_flow` | Destino + vuelo + reserva con descuento e impuesto = 950.0 |
| `test_pet_validation_error` | Rechazo de mascota en destino que no permite |
| `test_negative_price_rejected` | Rechazo de precios negativos (422) |
| `test_invalid_age_rejected` | Rechazo de edad invalida (422) |

---

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/api/v1/flights/destinations/` | Crear destino |
| GET | `/api/v1/flights/destinations/` | Listar destinos |
| POST | `/api/v1/flights/` | Crear vuelo |
| GET | `/api/v1/flights/` | Listar vuelos |
| POST | `/api/v1/bookings/` | Crear reserva |
| GET | `/api/v1/bookings/` | Listar reservas |
| POST | `/api/v1/ai/chat` | Chat con agente IA |
| POST | `/api/v1/ai/suggest-price` | Sugerencia de precios |

---

## Monitoreo y Depuracion

```bash
# Logs de todos los servicios
docker compose logs -f

# Logs solo del worker
docker compose logs -f worker

# Logs solo de la API
docker compose logs -f api

# Consola RabbitMQ: http://localhost:15672
# Usuario: admin  Password: admin123

# Shell Redis
docker compose exec redis redis-cli

# Shell PostgreSQL
docker compose exec db psql -U user -d flights
```

## Comandos Utiles

```bash
# Levantar todo
docker compose up --build -d

# Detener todo (datos de PostgreSQL se conservan)
docker compose down

# Reset completo (borra datos de la DB)
docker compose down -v && docker compose up --build -d

# Reconstruir solo la API
docker compose up --build api -d

# Estado de contenedores
docker compose ps

# Tests + reinicio de API
docker compose exec api pytest tests/ -v --tb=short && docker compose restart api
```

---

## Persistencia de Datos

PostgreSQL usa un **volumen nombrado** (`postgres_data`) definido en `docker-compose.yml`. Esto garantiza que los datos sobreviven a `docker compose down` y reinicios de contenedores.

- `docker compose down` → datos se conservan
- `docker compose down -v` → datos se eliminan (flag `-v` borra volumenes)

---

## Variables de Entorno

| Variable | Descripcion | Default |
|----------|-------------|---------|
| DATABASE_URL | Conexion PostgreSQL | `postgresql://user:pass@db:5432/flights` |
| RABBITMQ_URL | Conexion RabbitMQ | `pyamqp://admin:admin123@localhost:5672//` |
| REDIS_HOST | Host de Redis | `localhost` |
| REDIS_PORT | Puerto de Redis | `6379` |
| GROQ_API_KEY | API key de Groq (gratis) | - |

---

## CI/CD Pipeline

El pipeline (`.github/workflows/deploy.yml`) ejecuta:

1. **test** - Instala dependencias, levanta PostgreSQL, ejecuta pytest con `PYTHONPATH` configurado
2. **build-and-push** - Construye imagen Docker y sube a **ghcr.io** usando `GITHUB_TOKEN` (solo push a master)
3. **deploy** - Despliega en Kubernetes con Helm (solo si `KUBECONFIG` esta configurado)

### Secrets requeridos en GitHub

| Secret | Descripcion | Requerido |
|--------|-------------|-----------|
| `GITHUB_TOKEN` | Proporcionado automaticamente por GitHub Actions | Automatico |
| `KUBECONFIG` | Config de Kubernetes codificado en base64 | Solo para deploy |

> El registry usa **ghcr.io** (GitHub Container Registry) con autenticacion via `GITHUB_TOKEN`, eliminando la necesidad de configurar credenciales de registry externas.

---

## Docker

### Multi-stage Build

El `Dockerfile` usa dos etapas:

1. **Builder**: Instala dependencias de compilacion (`gcc`, `libpq-dev`) y compila pip packages
2. **Final**: Imagen limpia con solo las dependencias runtime, usuario no-root (`appuser`), healthcheck integrado

### Seguridad del contenedor

- Usuario no-root: `appuser` (no ejecuta como root)
- `--no-install-recommends`: imagen minima
- Healthcheck: `curl -f http://localhost:8000/` cada 30s