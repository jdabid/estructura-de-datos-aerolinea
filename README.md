# Flight Reservation System

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3-FF6600?logo=rabbitmq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Helm-326CE5?logo=kubernetes&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?logo=langchain&logoColor=white)

Sistema de reservas de vuelos con arquitectura moderna, procesamiento asincrono y agente de IA. Construido con Vertical Slice Architecture + CQRS, contenedorizado con Docker, orquestado con Kubernetes + Helm, y un pipeline CI/CD de 3 etapas.

---

## Tabla de Contenidos

- [Stack Tecnologico](#stack-tecnologico)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Logica de Negocio](#logica-de-negocio)
- [Agente de IA - Patron RAG](#agente-de-ia---patron-rag)
- [Message Queue y Background Processing](#message-queue-y-background-processing)
- [Inicio Rapido](#inicio-rapido)
- [Guia de Uso Completa](#guia-de-uso-completa)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Docker](#docker)
- [Kubernetes y Helm](#kubernetes-y-helm)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoreo y Depuracion](#monitoreo-y-depuracion)
- [Variables de Entorno](#variables-de-entorno)
- [Documentacion del Proyecto](#documentacion-del-proyecto)

---

## Stack Tecnologico

| Capa | Tecnologia | Proposito |
|------|------------|-----------|
| API | Python 3.11, FastAPI, Pydantic v2 | REST API con validacion automatica |
| Base de datos | PostgreSQL 15 | Persistencia relacional con volumen |
| Cache / Stats | Redis 7 | Contadores, estadisticas en tiempo real |
| Message Broker | RabbitMQ 3 | Cola de mensajes para eventos asincronos |
| Worker | Celery 5 | Procesamiento en segundo plano |
| AI Agent | LangChain + Groq (Llama 3.3 70B) | Agente RAG con datos reales |
| Contenedores | Docker (multi-stage, non-root) | Build optimizado y seguro |
| Orquestacion | Kubernetes + Helm Charts (HPA) | Autoescalado horizontal |
| CI/CD | GitHub Actions + ghcr.io | Pipeline automatizado de 3 etapas |

---

## Arquitectura

### Patron: Vertical Slice Architecture + CQRS

Cada feature es un modulo autocontenido con sus propios modelos, schemas, commands (escritura) y queries (lectura). Esto reduce el acoplamiento entre features y permite que cada modulo evolucione independientemente.

```
                         ┌──────────────┐
                         │   FastAPI    │
                         │   Gateway    │
                         └──┬────┬────┬─┘
                            │    │    │
               ┌────────────┘    │    └────────────┐
               ▼                 ▼                 ▼
        ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
        │   Flights    │  │  Bookings   │  │  AI Agent   │
        │   (Slice)    │  │   (Slice)   │  │   (Slice)   │
        │             │  │             │  │             │
        │ models.py   │  │ models.py   │  │ agent.py    │
        │ schemas.py  │  │ schemas.py  │  │ tools.py    │
        │ commands.py │  │ commands.py │  │             │
        │ queries.py  │  │ queries.py  │  │             │
        └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
               │                │                 │
               ▼                ▼                 ▼
        ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
        │ PostgreSQL  │  │  RabbitMQ   │  │  Groq LLM   │
        │             │  │  (Broker)   │  │ (Llama 3.3) │
        └─────────────┘  └──────┬──────┘  └─────────────┘
                                │
                         ┌──────▼──────┐
                         │   Celery    │
                         │   Worker    │
                         └──────┬──────┘
                                │
                         ┌──────▼──────┐
                         │    Redis    │
                         │   (Stats)   │
                         └─────────────┘
```

### CQRS (Command Query Responsibility Segregation)

| Tipo | Archivo | Responsabilidad |
|------|---------|-----------------|
| **Command** | `commands.py` | Operaciones de escritura: crear, actualizar, eliminar |
| **Query** | `queries.py` | Operaciones de lectura: listar, buscar, filtrar |

---

## Estructura del Proyecto

```
flight-reservation-system/
│
├── src/
│   ├── main.py                          # Entry point FastAPI
│   ├── api/v1/
│   │   ├── flights.py                   # Rutas de vuelos y destinos
│   │   ├── bookings.py                  # Rutas de reservas
│   │   └── ai.py                        # Rutas del agente IA (RAG)
│   ├── features/
│   │   ├── flights/
│   │   │   ├── models.py                # ORM: Destination, Flight
│   │   │   ├── schemas.py               # Schemas Pydantic v2
│   │   │   ├── commands.py              # Crear destino, crear vuelo
│   │   │   └── queries.py               # Listar vuelos, destinos
│   │   ├── bookings/
│   │   │   ├── models.py                # ORM: Booking
│   │   │   ├── schemas.py               # Schemas Pydantic v2
│   │   │   ├── commands.py              # Crear reserva (precio, descuento, impuesto)
│   │   │   └── queries.py               # Listar reservas
│   │   └── ai/
│   │       ├── agent.py                 # Singleton LLM (ChatGroq + lru_cache)
│   │       └── tools.py                 # Tools: market data (PG), demand stats (Redis)
│   ├── shared/
│   │   ├── database.py                  # SQLAlchemy 2.0 engine + SessionLocal
│   │   └── redis_client.py              # Cliente Redis (incrbyfloat, lpush, scan)
│   └── worker/
│       ├── celery_app.py                # Configuracion Celery + RabbitMQ
│       └── tasks.py                     # Task: process_booking_event (max_retries=3)
│
├── tests/
│   └── test_integration.py              # Tests de integracion
│
├── infra/
│   ├── docker/
│   │   └── Dockerfile                   # Multi-stage build (non-root: appuser)
│   └── helm/flight-app/
│       ├── Chart.yaml                   # Helm chart v1.0.0
│       ├── values.yaml                  # Config: replicas, HPA, resources, env
│       └── templates/
│           ├── deployment.yaml          # Deployment API + Worker + HPA
│           ├── service.yaml             # ClusterIP port 8000
│           └── configmap.yaml           # ConfigMap + Secret
│
├── .github/workflows/
│   └── deploy.yml                       # CI/CD: test → build → deploy
│
├── evaluacion-tecnica/                  # Evaluacion arquitectonica del proyecto
│   ├── evaluacion-proyecto.md           # Analisis tecnico como Senior Architect
│   ├── cronograma-transformacion.md     # Plan de transformacion en 10 fases
│   └── cronograma-scrum.md              # Cronograma Scrum: 7 sprints, 53 user stories
│
├── LEARNING/
│   └── questions.md                     # 20 preguntas tecnicas de entrevista
│
├── docker-compose.yml                   # Orquestacion: 5 servicios
├── requirements.txt                     # Dependencias Python
└── README.md
```

---

## Logica de Negocio

### Flujo de Reserva

```
1. Crear destino    →  nombre, impuesto, promocion, mascotas
2. Crear vuelo      →  numero, origen, precio base, destino
3. Crear reserva    →  pasajero, edad, mascota, vuelo
                         │
                         ▼
                    ┌─────────────────────────────┐
                    │  Calcular precio             │
                    │                              │
                    │  Si promocion:               │
                    │    precio = base * 0.90      │
                    │  Sino:                       │
                    │    precio = base             │
                    │                              │
                    │  total = precio + tax_amount │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  Validaciones                 │
                    │                              │
                    │  - Mascota + destino no      │
                    │    permite? → HTTP 400       │
                    │  - Edad < 0 o > 150?         │
                    │    → HTTP 422                │
                    │  - Precio <= 0?              │
                    │    → HTTP 422                │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  Evento Asincrono            │
                    │                              │
                    │  Celery → RabbitMQ → Worker  │
                    │  → Redis (stats)             │
                    └──────────────────────────────┘
```

### Reglas de Negocio

| Regla | Descripcion |
|-------|-------------|
| Descuento promocion | Si `is_promotion: true` → 10% descuento sobre `base_price` |
| Impuesto por destino | Se suma `tax_amount` del destino al precio |
| Validacion mascotas | Si `has_pet: true` y destino no permite → HTTP 400 |
| Validacion edad | `passenger_age` entre 0 y 150 (Pydantic `field_validator`) |
| Validacion precio | `base_price` debe ser > 0 (Pydantic `field_validator`) |
| Infantes | Edad < 12: dulce de cortesia ($5.0) registrado en Redis |

### Formula de Precio

```
total_price = (base_price * 0.90 si hay promocion, o base_price) + tax_amount
```

**Ejemplo:** base_price=1000, promocion=true, tax=50 → `1000 * 0.90 + 50 = 950.0`

---

## Agente de IA - Patron RAG

El sistema implementa un agente de IA usando **RAG (Retrieval-Augmented Generation)**:

```
Usuario
   │
   ▼
┌──────────────────────────────────────────────────────┐
│                    API FastAPI                        │
│                                                      │
│  1. RETRIEVAL                                        │
│     ├── get_flight_market_data() → PostgreSQL        │
│     │   (precio base, impuestos, promocion)          │
│     └── get_demand_stats() → Redis                   │
│         (popularidad destinos, ingresos, infantes)   │
│                                                      │
│  2. AUGMENTATION                                     │
│     └── Prompt = datos reales + pregunta usuario     │
│                                                      │
│  3. GENERATION                                       │
│     └── Groq (Llama 3.3 70B) → respuesta            │
└──────────────────────────────────────────────────────┘
   │
   ▼
Respuesta contextualizada con datos reales
```

### Endpoints IA

| Endpoint | Descripcion |
|----------|-------------|
| `POST /api/v1/ai/chat` | Chatbot general sobre vuelos, impuestos, mascotas |
| `POST /api/v1/ai/suggest-price` | Analista de precios con recomendaciones basadas en demanda |

### Decisiones Tecnicas IA

| Decision | Implementacion |
|----------|----------------|
| Singleton LLM | `@functools.lru_cache(maxsize=1)` evita conexiones redundantes |
| Tools LangChain | `@tool` decorator para recuperar datos de PostgreSQL y Redis |
| Prompt en espanol | Todas las respuestas del agente son en espanol |

---

## Message Queue y Background Processing

### Flujo Asincrono

```
[POST /bookings/]
       │
       ▼
[Crear reserva en PostgreSQL]
       │
       ▼
[Responder al usuario inmediatamente]
       │
       ▼ (async)
[process_booking_event.delay(payload)]
       │
       ▼
[RabbitMQ Queue]
       │
       ▼
[Celery Worker consume el mensaje]
       │
       ├── stats:total_revenue         (+total_price)
       ├── stats:destination:{nombre}  (+1 popularidad)
       ├── stats:total_pet_bookings    (+1 si mascota)
       ├── stats:total_candy_cost      (+5.0 si infante)
       ├── stats:total_infant_count    (+1 si infante)
       └── logs:candy_distribution     (log de dulce)
```

### Configuracion Celery

| Parametro | Valor | Proposito |
|-----------|-------|-----------|
| `task_acks_late` | `True` | ACK despues de completar (no se pierden tareas) |
| `worker_prefetch_multiplier` | `1` | Un mensaje a la vez (distribucion equitativa) |
| `max_retries` | `3` | Reintentos automaticos en caso de fallo |
| `default_retry_delay` | `10s` | Espera entre reintentos |

---

## Inicio Rapido

### Requisitos Previos

- Docker y Docker Compose instalados
- GROQ_API_KEY (gratis en [console.groq.com](https://console.groq.com)) — solo para endpoints `/ai/*`

```bash
docker --version          # Docker 20+ requerido
docker compose version    # Compose v2+ requerido
```

### 1. Clonar el repositorio

```bash
git clone https://github.com/jdabid/flight-reservation-system.git
cd flight-reservation-system
```

### 2. Crear archivo `.env`

```bash
echo "GROQ_API_KEY=gsk-tu-clave-aqui" > .env
```

### 3. Levantar todos los servicios

```bash
docker compose up --build -d
```

### 4. Verificar

```bash
docker compose ps       # Todos deben mostrar "Up (healthy)"
curl http://localhost:8000/
```

Respuesta esperada:

```json
{"status": "ok", "message": "Sistema con Agente de IA Operativo"}
```

### Servicios

| Servicio | Puerto | Descripcion |
|----------|--------|-------------|
| api | 8000 | FastAPI (uvicorn) |
| worker | — | Celery worker |
| db | 5432 | PostgreSQL 15 (volumen persistente) |
| redis | 6379 | Redis 7 |
| rabbitmq | 5672 / 15672 | RabbitMQ + Management UI |

---

## Guia de Uso Completa

### Paso 1 — Crear un destino

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

### Paso 2 — Crear un vuelo

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

### Paso 3 — Crear una reserva

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

**Precio esperado:** `1000 * 0.90 + 50 = 950.0`

### Paso 4 — Verificar estadisticas en Redis

```bash
docker compose exec redis redis-cli GET stats:total_revenue
docker compose exec redis redis-cli GET stats:destination:Cartagena
docker compose exec redis redis-cli GET stats:total_candy_cost
docker compose exec redis redis-cli GET stats:total_infant_count
docker compose exec redis redis-cli GET stats:total_pet_bookings
```

### Paso 5 — Validacion de mascotas (error esperado)

```bash
# Crear destino que no permite mascotas
curl -X POST http://localhost:8000/api/v1/flights/destinations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Londres", "tax_amount": 100, "is_promotion": false, "allows_pets": false}'

# Crear vuelo a ese destino
curl -X POST http://localhost:8000/api/v1/flights/ \
  -H "Content-Type: application/json" \
  -d '{"flight_number": "LON-99", "origin": "Bogota", "base_price": 2000, "destination_id": 2}'

# Intentar reserva con mascota → HTTP 400
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"passenger_name": "Test User", "passenger_age": 25, "has_pet": true, "flight_id": 2}'
```

Respuesta: `{"detail": "El destino Londres no acepta mascotas."}`

### Paso 6 — Reserva de infante (dulce automatico)

```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"passenger_name": "Pedrito", "passenger_age": 8, "has_pet": false, "flight_id": 1}'

# Verificar dulce en Redis
docker compose exec redis redis-cli LRANGE logs:candy_distribution 0 -1
```

### Paso 7 — Agente de IA (requiere GROQ_API_KEY)

```bash
# Chat general
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Cuanto cuestan los impuestos para viajar a Cartagena?"}'

# Sugerencia de precios
curl -X POST http://localhost:8000/api/v1/ai/suggest-price \
  -H "Content-Type: application/json" \
  -d '{"destination_name": "Cartagena"}'
```

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

Documentacion interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testing

### Ejecutar tests

```bash
# Dentro de Docker (recomendado)
docker compose exec api pytest tests/ -v --tb=short

# Reiniciar API despues de tests
docker compose restart api
```

```bash
# Local (requiere DB y Redis corriendo)
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

## Docker

### Multi-stage Build

El Dockerfile usa dos etapas para optimizar el tamano de la imagen:

```
Etapa 1: Builder                    Etapa 2: Final
┌────────────────────┐              ┌────────────────────┐
│ python:3.11-slim   │              │ python:3.11-slim   │
│                    │              │                    │
│ + gcc, libpq-dev   │   COPY      │ Solo runtime deps  │
│ + pip install      │ ─────────►  │ Usuario: appuser   │
│ + compilacion      │  wheels     │ Healthcheck        │
│                    │              │ Puerto: 8000       │
│ ~1.2GB             │              │ ~200MB             │
└────────────────────┘              └────────────────────┘
```

### Seguridad del Contenedor

- Usuario no-root: `appuser` (no ejecuta como root)
- `--no-install-recommends`: imagen minima
- Healthcheck: `curl -f http://localhost:8000/` cada 30s

### Comandos Docker

```bash
docker compose up --build -d              # Levantar todo
docker compose down                       # Detener (datos se conservan)
docker compose down -v                    # Reset completo (borra datos)
docker compose up --build api -d          # Reconstruir solo API
docker compose logs -f api                # Logs de la API
docker compose logs -f worker             # Logs del worker
```

---

## Kubernetes y Helm

### Helm Chart

El chart `flight-app` despliega la aplicacion completa en Kubernetes:

```bash
# Instalar/actualizar
helm upgrade --install flight-system ./infra/helm/flight-app

# Verificar
helm list
kubectl get pods
```

### Recursos Desplegados

| Recurso | Descripcion |
|---------|-------------|
| Deployment (API) | FastAPI con readiness/liveness probes |
| Deployment (Worker) | Celery worker (condicional) |
| Service | ClusterIP en puerto 8000 |
| HPA | Autoescalado: min 2, max 10 replicas, target CPU 70% |
| ConfigMap | Variables no sensibles (DATABASE_URL, REDIS_HOST) |
| Secret | Variables sensibles (GROQ_API_KEY) |

### Autoescalado (HPA)

```
Replicas:  2 ◄──── minimo (alta disponibilidad)
           │
           │  CPU > 70% → escala UP
           │  CPU < 70% → escala DOWN
           │
          10 ◄──── maximo
```

---

## CI/CD Pipeline

El pipeline (`.github/workflows/deploy.yml`) ejecuta 3 etapas:

```
┌─────────┐     ┌────────────────┐     ┌──────────┐
│  TEST   │────►│ BUILD & PUSH   │────►│  DEPLOY  │
│         │     │                │     │          │
│ pytest  │     │ Docker build   │     │ Helm     │
│ PG svc  │     │ Push ghcr.io   │     │ upgrade  │
│         │     │ (solo master)  │     │ (si K8s) │
└─────────┘     └────────────────┘     └──────────┘
```

| Etapa | Trigger | Descripcion |
|-------|---------|-------------|
| **Test** | push/PR | pytest con PostgreSQL service en GitHub Actions |
| **Build & Push** | push a master | Imagen Docker → ghcr.io con SHA como tag |
| **Deploy** | push a master | Helm upgrade al cluster (requiere KUBECONFIG) |

### Secrets Requeridos

| Secret | Descripcion |
|--------|-------------|
| `GITHUB_TOKEN` | Automatico (GitHub Actions) |
| `KUBECONFIG` | Base64 del kubeconfig (solo para deploy) |

---

## Monitoreo y Depuracion

```bash
# Logs de todos los servicios
docker compose logs -f

# Logs especificos
docker compose logs -f api
docker compose logs -f worker

# Consola RabbitMQ
# http://localhost:15672  (admin / admin123)

# Shell Redis
docker compose exec redis redis-cli

# Shell PostgreSQL
docker compose exec db psql -U user -d flights

# Estado de contenedores
docker compose ps
```

---

## Variables de Entorno

| Variable | Descripcion | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Conexion PostgreSQL | `postgresql://user:pass@db:5432/flights` |
| `RABBITMQ_URL` | Conexion RabbitMQ | `pyamqp://admin:admin123@localhost:5672//` |
| `REDIS_HOST` | Host de Redis | `localhost` |
| `REDIS_PORT` | Puerto de Redis | `6379` |
| `GROQ_API_KEY` | API key de Groq (gratis) | — (requerido para IA) |

---

## Persistencia de Datos

PostgreSQL usa un volumen nombrado (`postgres_data`):

| Comando | Datos |
|---------|-------|
| `docker compose down` | Se conservan |
| `docker compose down -v` | Se eliminan (flag `-v` borra volumenes) |

---

## Documentacion del Proyecto

| Documento | Ubicacion | Contenido |
|-----------|-----------|-----------|
| Evaluacion tecnica | `evaluacion-tecnica/evaluacion-proyecto.md` | Analisis como Senior Architect: nivel, fortalezas, debilidades |
| Plan de transformacion | `evaluacion-tecnica/cronograma-transformacion.md` | 10 fases para fullstack con React, Terraform, observabilidad |
| Cronograma Scrum | `evaluacion-tecnica/cronograma-scrum.md` | 7 sprints, 53 user stories, 229 story points |
| Cronograma MVP | `schelude/cronograma.md` | Plan original de desarrollo en 6 semanas |
| Preguntas tecnicas | `LEARNING/questions.md` | 20 preguntas de entrevista con respuestas |
| Propuesta arquitectonica | `propuesta-arquitectonica.md` | Propuesta tecnica inicial del proyecto |
| Descripcion detallada | `description-questions-project.md` | Enunciado + 20 Q&A + roles para empleo |

---

## Tecnologias Demostradas

| Area | Tecnologias |
|------|-------------|
| **Backend** | Python, FastAPI, SQLAlchemy 2.0, Pydantic v2, Celery |
| **Arquitectura** | Vertical Slice, CQRS, Event-Driven, RAG Pattern |
| **Base de datos** | PostgreSQL, Redis |
| **Mensajeria** | RabbitMQ, Celery tasks con retries |
| **IA** | LangChain, Groq, Llama 3.3 70B, RAG |
| **DevOps** | Docker multi-stage, Kubernetes, Helm, HPA |
| **CI/CD** | GitHub Actions, ghcr.io |
| **Seguridad** | Non-root containers, healthchecks |
