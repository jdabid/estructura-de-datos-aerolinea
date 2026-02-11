 # Flight Reservation System                                                                                                                                                                                                      
                                                                                                                                                                                                                                   
  Sistema de reserva de vuelos con arquitectura moderna, procesamiento asincrono y capacidades de IA.                                                                                                                              

  ## Stack Tecnologico

  | Capa | Tecnologia |
  |------|------------|
  | API | Python 3.11, FastAPI, Pydantic v2 |
  | Base de datos | PostgreSQL 15 |
  | Cache / Stats | Redis 7 |
  | Message Broker | RabbitMQ 3 |
  | Worker | Celery 5 |
  | AI Agent | LangChain + OpenAI (GPT-3.5-turbo) |
  | Contenedores | Docker (multi-stage build) |
  | Orquestacion | Kubernetes + Helm Charts |
  | CI/CD | GitHub Actions |

  ## Arquitectura

  Vertical Slice Architecture + CQRS

  src/
  ├── main.py                          # FastAPI app entry point
  ├── api/v1/
  │   ├── flights.py                   # Rutas de vuelos y destinos
  │   ├── bookings.py                  # Rutas de reservas
  │   └── ai.py                        # Rutas del agente de IA
  ├── features/
  │   ├── flights/
  │   │   ├── models.py                # ORM: Destination, Flight
  │   │   ├── schemas.py               # Schemas Pydantic
  │   │   ├── commands.py              # Escritura: crear destino, crear vuelo
  │   │   └── queries.py               # Lectura: listar vuelos
  │   ├── bookings/
  │   │   ├── models.py                # ORM: Booking
  │   │   ├── schemas.py               # Schemas Pydantic
  │   │   ├── commands.py              # Logica de negocio: precio, descuento, impuesto
  │   │   └── queries.py               # Lectura: listar reservas
  │   └── ai/
  │       ├── agent.py                 # Agente LangChain
  │       └── tools.py                 # Tools: market data, demand stats
  ├── shared/
  │   ├── database.py                  # SQLAlchemy engine + SessionLocal
  │   └── redis_client.py              # Cliente Redis
  └── worker/
      ├── celery_app.py                # Configuracion Celery
      └── tasks.py                     # Task: process_booking_event

  infra/
  ├── docker/Dockerfile                # Build multi-stage (usuario no-root)
  └── helm/flight-app/templates/
      └── deployment.yaml              # Deployment + HPA

  tests/
  └── test_integration.py              # Tests de integracion

  .github/workflows/
  └── deploy.yml                       # Pipeline CI/CD

  ## Logica de Negocio

  Al crear una reserva el sistema aplica:

  1. **Descuento por promocion**: si el destino tiene `is_promotion: true` aplica 10% de descuento sobre `base_price`
  2. **Impuesto por destino**: suma `tax_amount` del destino al precio
  3. **Validacion de mascotas**: si `has_pet: true` y el destino no permite mascotas rechaza con 400
  4. **Evento asincrono**: Celery actualiza en Redis recaudo total, popularidad, dulces para infantes < 12 anios

  **Formula:** `total_price = (base_price * 0.90 si promocion) + tax_amount`

  ---

  ## Requisitos Previos

  - Docker y Docker Compose instalados
  - OPENAI_API_KEY valida (solo para endpoints `/ai/*`)

  ```bash
  docker --version
  docker compose version

  ---
  Paso a Paso: Ejecutar la Aplicacion

  1. Clonar el repositorio

  git clone https://github.com/jdabid/flight-reservation-system.git
  cd flight-reservation-system

  2. Crear archivo .env

  cat <<'EOF' > .env
  DATABASE_URL=postgresql://user:pass@db:5432/flights
  RABBITMQ_URL=pyamqp://admin:admin123@rabbitmq:5672//
  REDIS_HOST=redis
  OPENAI_API_KEY=sk-tu-clave-aqui
  EOF

  3. Levantar todos los servicios

  docker compose up --build -d

  Esto levanta 5 contenedores:
  ┌──────────┬──────────────┬──────────────────────────┐
  │ Servicio │    Puerto    │       Descripcion        │
  ├──────────┼──────────────┼──────────────────────────┤
  │ api      │ 8000         │ FastAPI (uvicorn)        │
  ├──────────┼──────────────┼──────────────────────────┤
  │ worker   │ -            │ Celery worker            │
  ├──────────┼──────────────┼──────────────────────────┤
  │ db       │ 5432         │ PostgreSQL 15            │
  ├──────────┼──────────────┼──────────────────────────┤
  │ redis    │ 6379         │ Redis 7                  │
  ├──────────┼──────────────┼──────────────────────────┤
  │ rabbitmq │ 5672 / 15672 │ RabbitMQ + Management UI │
  └──────────┴──────────────┴──────────────────────────┘
  4. Verificar que todo esta corriendo

  docker compose ps

  5. Health check

  curl http://localhost:8000/

  Respuesta esperada:

  {"status": "ok", "message": "Sistema con Agente de IA Operativo"}

  6. Documentacion interactiva

  Abrir en el navegador: http://localhost:8000/docs

  ---
  Paso a Paso: Probar el Flujo Completo

  Paso 1 - Crear un destino

  curl -X POST http://localhost:8000/api/v1/flights/destinations/ \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Cartagena",
      "tax_amount": 50.0,
      "is_promotion": true,
      "allows_pets": true
    }'

  Paso 2 - Crear un vuelo

  curl -X POST http://localhost:8000/api/v1/flights/ \
    -H "Content-Type: application/json" \
    -d '{
      "flight_number": "CT-123",
      "origin": "Bogota",
      "base_price": 1000.0,
      "destination_id": 1
    }'

  Paso 3 - Crear una reserva (precio esperado: 950)

  curl -X POST http://localhost:8000/api/v1/bookings/ \
    -H "Content-Type: application/json" \
    -d '{
      "passenger_name": "Juan Perez",
      "passenger_age": 30,
      "has_pet": true,
      "flight_id": 1
    }'

  Calculo: 1000 * 0.90 + 50 = 950.0

  Paso 4 - Verificar el worker

  docker compose logs worker --tail 20

  Paso 5 - Consultar estadisticas en Redis

  docker compose exec redis redis-cli GET stats:total_revenue
  docker compose exec redis redis-cli GET stats:destination:Cartagena
  docker compose exec redis redis-cli GET stats:total_candy_cost
  docker compose exec redis redis-cli GET stats:total_infant_count
  docker compose exec redis redis-cli GET stats:total_pet_bookings

  Paso 6 - Probar validacion de mascotas (debe dar error 400)

  curl -X POST http://localhost:8000/api/v1/flights/destinations/ \
    -H "Content-Type: application/json" \
    -d '{"name": "Londres", "tax_amount": 100, "is_promotion": false, "allows_pets": false}'

  curl -X POST http://localhost:8000/api/v1/flights/ \
    -H "Content-Type: application/json" \
    -d '{"flight_number": "LON-99", "origin": "Bogota", "base_price": 2000, "destination_id": 2}'

  curl -X POST http://localhost:8000/api/v1/bookings/ \
    -H "Content-Type: application/json" \
    -d '{"passenger_name": "Test User", "passenger_age": 25, "has_pet": true, "flight_id": 2}'

  Respuesta esperada:

  {"detail": "El destino Londres no acepta mascotas."}

  Paso 7 - Probar reserva de infante (dulce automatico)

  curl -X POST http://localhost:8000/api/v1/bookings/ \
    -H "Content-Type: application/json" \
    -d '{"passenger_name": "Pedrito", "passenger_age": 8, "has_pet": false, "flight_id": 1}'

  Verificar dulce en Redis:

  docker compose exec redis redis-cli LRANGE logs:candy_distribution 0 -1

  Paso 8 - Probar el agente de IA (requiere OPENAI_API_KEY)

  curl -X POST http://localhost:8000/api/v1/ai/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Cuanto cuestan los impuestos para viajar a Cartagena?"}'

  curl -X POST http://localhost:8000/api/v1/ai/suggest-price \
    -H "Content-Type: application/json" \
    -d '{"destination_name": "Cartagena"}'

  ---
  Ejecutar Tests

  Opcion A - Dentro de Docker (recomendado)

  docker compose exec api pytest tests/ -v --tb=short

  Opcion B - Local con la DB del compose

  docker compose up db redis -d

  pip install -r requirements.txt

  DATABASE_URL=postgresql://user:pass@localhost:5432/flights \
  REDIS_HOST=localhost \
  RABBITMQ_URL="" \
  pytest tests/ -v --tb=short

  Tests incluidos
  ┌──────────────────────────────┬────────────────────────────────────────────────────────────┐
  │             Test             │                           Valida                           │
  ├──────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ test_full_booking_flow       │ Destino + vuelo + reserva con descuento e impuesto = 950.0 │
  ├──────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ test_pet_validation_error    │ Rechazo de mascota en destino que no permite               │
  ├──────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ test_negative_price_rejected │ Rechazo de precios negativos (422)                         │
  ├──────────────────────────────┼────────────────────────────────────────────────────────────┤
  │ test_invalid_age_rejected    │ Rechazo de edad invalida (422)                             │
  └──────────────────────────────┴────────────────────────────────────────────────────────────┘
  ---
  Endpoints
  ┌────────┬───────────────────────────────┬───────────────────────┐
  │ Metodo │             Ruta              │      Descripcion      │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ GET    │ /                             │ Health check          │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ POST   │ /api/v1/flights/destinations/ │ Crear destino         │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ GET    │ /api/v1/flights/destinations/ │ Listar destinos       │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ POST   │ /api/v1/flights/              │ Crear vuelo           │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ GET    │ /api/v1/flights/              │ Listar vuelos         │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ POST   │ /api/v1/bookings/             │ Crear reserva         │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ GET    │ /api/v1/bookings/             │ Listar reservas       │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ POST   │ /api/v1/ai/chat               │ Chat con agente IA    │
  ├────────┼───────────────────────────────┼───────────────────────┤
  │ POST   │ /api/v1/ai/suggest-price      │ Sugerencia de precios │
  └────────┴───────────────────────────────┴───────────────────────┘
  ---
  Monitoreo y Depuracion

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

  Comandos Utiles

  # Levantar todo
  docker compose up --build -d

  # Detener todo
  docker compose down

  # Reset completo (borra datos de la DB)
  docker compose down -v && docker compose up --build -d

  # Reconstruir solo la API
  docker compose up --build api -d

  # Estado de contenedores
  docker compose ps

  ---
  Variables de Entorno
  ┌────────────────┬─────────────────────┬──────────────────────────────────────────┐
  │    Variable    │     Descripcion     │                 Default                  │
  ├────────────────┼─────────────────────┼──────────────────────────────────────────┤
  │ DATABASE_URL   │ Conexion PostgreSQL │ postgresql://user:pass@db:5432/flights   │
  ├────────────────┼─────────────────────┼──────────────────────────────────────────┤
  │ RABBITMQ_URL   │ Conexion RabbitMQ   │ pyamqp://admin:admin123@localhost:5672// │
  ├────────────────┼─────────────────────┼──────────────────────────────────────────┤
  │ REDIS_HOST     │ Host de Redis       │ localhost                                │
  ├────────────────┼─────────────────────┼──────────────────────────────────────────┤
  │ REDIS_PORT     │ Puerto de Redis     │ 6379                                     │
  ├────────────────┼─────────────────────┼──────────────────────────────────────────┤
  │ OPENAI_API_KEY │ API key de OpenAI   │ -                                        │
  └────────────────┴─────────────────────┴──────────────────────────────────────────┘
  ---
  CI/CD Pipeline

  El pipeline (.github/workflows/deploy.yml) ejecuta:

  1. test - Instala dependencias, levanta PostgreSQL, ejecuta pytest
  2. build-and-push - Construye imagen Docker y sube al registry (solo push a master)
  3. deploy - Despliega en Kubernetes con Helm

  Secrets requeridos en GitHub:

  - REGISTRY_URL
  - REGISTRY_USER
  - REGISTRY_PASSWORD
  - KUBECONFIG (base64 encoded)

  ---
