# Cronograma de Transformacion: Flight Reservation System

> Plan general para transformar el proyecto en una aplicacion fullstack de nivel profesional.

---

## Stack Tecnologico Definido

### Backend
| Capa | Tecnologia |
|------|------------|
| Lenguaje | Python 3.12 |
| Framework API | FastAPI |
| ORM | SQLAlchemy 2.0 + Alembic (migraciones) |
| Validacion | Pydantic v2 |
| Autenticacion | JWT (python-jose + passlib) |
| Base de datos | PostgreSQL 16 |
| Cache | Redis 7 |
| Message Broker | RabbitMQ 3 |
| Worker | Celery 5 |
| Testing | pytest + pytest-cov + httpx |
| Linting | Ruff + mypy |

### Frontend
| Capa | Tecnologia |
|------|------------|
| Framework | React 18 + TypeScript |
| Build tool | Vite |
| State management | Zustand |
| HTTP client | Axios / TanStack Query |
| Routing | React Router v6 |
| UI Components | Tailwind CSS + shadcn/ui |
| Testing | Vitest + React Testing Library |

### IA / Agente Inteligente
| Capa | Tecnologia |
|------|------------|
| Framework | LangChain |
| LLM Provider | Groq (Llama 3.3 70B) |
| Patron | RAG (Retrieval-Augmented Generation) |
| Embeddings | sentence-transformers (local) o OpenAI Embeddings |
| Vector Store | pgvector (extension de PostgreSQL) |
| Propuesta avanzada | Fine-tuning con datos historicos de reservas para prediccion de demanda |

### Infraestructura
| Capa | Tecnologia |
|------|------------|
| Contenedores | Docker (multi-stage builds) |
| Orquestacion local | Docker Compose |
| Orquestacion produccion | Kubernetes |
| Empaquetado K8s | Helm Charts |
| Config por ambiente | Kustomize |
| IaC | Terraform (AWS) |
| CI/CD | GitHub Actions |
| Registry | ghcr.io |
| Observabilidad | Prometheus + Grafana + OpenTelemetry |

---

## Arquitectura General

```
                    ┌─────────────┐
                    │   React UI  │
                    │  (Vite+TS)  │
                    └──────┬──────┘
                           │ HTTP/REST
                    ┌──────▼──────┐
                    │   FastAPI   │
                    │  (Gateway)  │
                    └──┬───┬───┬──┘
                       │   │   │
          ┌────────────┘   │   └────────────┐
          ▼                ▼                ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │  Flights  │   │ Bookings  │   │  AI Agent  │
    │  (Slice)  │   │  (Slice)  │   │  (Slice)   │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │               │               │
          ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │ PostgreSQL│   │ RabbitMQ  │   │  Groq LLM │
    │ + pgvector│   │  (Broker) │   │ (Llama 3) │
    └───────────┘   └─────┬─────┘   └───────────┘
                          │
                    ┌─────▼─────┐
                    │  Celery   │
                    │  Worker   │
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │   Redis   │
                    │  (Stats)  │
                    └───────────┘
```

### Patron Arquitectonico: Vertical Slice + CQRS

Cada feature es un modulo autocontenido:
- **Commands** — operaciones de escritura (crear, actualizar, eliminar)
- **Queries** — operaciones de lectura (listar, buscar, filtrar)
- **Models** — entidades SQLAlchemy
- **Schemas** — validacion Pydantic v2

### Message Queue & Background Processing

```
[API Request] → [Create Booking] → [Commit DB] → [Response al usuario]
                                         │
                                         ▼
                                  [RabbitMQ Queue]
                                         │
                                         ▼
                                  [Celery Worker]
                                    ├── Actualizar stats en Redis
                                    ├── Calcular metricas de demanda
                                    ├── Registrar dulces para infantes
                                    ├── Enviar notificaciones
                                    └── Alimentar datos para IA
```

---

## Estructura de Carpetas

```
flight-reservation-system/
│
├── backend/
│   ├── src/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── flights.py
│   │   │       ├── bookings.py
│   │   │       ├── auth.py
│   │   │       ├── ai.py
│   │   │       └── stats.py
│   │   ├── features/
│   │   │   ├── flights/
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── commands.py
│   │   │   │   └── queries.py
│   │   │   ├── bookings/
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── commands.py
│   │   │   │   └── queries.py
│   │   │   ├── auth/
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── commands.py
│   │   │   │   ├── queries.py
│   │   │   │   └── jwt.py
│   │   │   ├── ai/
│   │   │   │   ├── agent.py
│   │   │   │   ├── tools.py
│   │   │   │   └── embeddings.py
│   │   │   └── stats/
│   │   │       ├── schemas.py
│   │   │       └── queries.py
│   │   ├── shared/
│   │   │   ├── database.py
│   │   │   ├── redis_client.py
│   │   │   ├── exceptions.py
│   │   │   └── middleware.py
│   │   └── worker/
│   │       ├── celery_app.py
│   │       └── tasks.py
│   ├── alembic/
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── versions/
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_flights_commands.py
│   │   │   ├── test_flights_queries.py
│   │   │   ├── test_bookings_commands.py
│   │   │   ├── test_bookings_queries.py
│   │   │   ├── test_auth.py
│   │   │   └── test_schemas.py
│   │   └── integration/
│   │       ├── test_booking_flow.py
│   │       ├── test_flight_flow.py
│   │       └── test_ai_agent.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Flights.tsx
│   │   │   ├── Bookings.tsx
│   │   │   ├── Stats.tsx
│   │   │   └── AiChat.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── FlightCard.tsx
│   │   │   ├── BookingForm.tsx
│   │   │   ├── StatsPanel.tsx
│   │   │   └── ChatWindow.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── flights.ts
│   │   ├── stores/
│   │   │   ├── authStore.ts
│   │   │   └── flightStore.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.monitoring.yml
│   │   └── docker-compose.dev.yml
│   ├── kubernetes/
│   │   ├── helm/
│   │   │   └── flight-app/
│   │   │       ├── Chart.yaml
│   │   │       ├── values.yaml
│   │   │       └── templates/
│   │   │           ├── deployment-api.yaml
│   │   │           ├── deployment-worker.yaml
│   │   │           ├── deployment-frontend.yaml
│   │   │           ├── service.yaml
│   │   │           ├── ingress.yaml
│   │   │           ├── configmap.yaml
│   │   │           ├── secret.yaml
│   │   │           ├── hpa.yaml
│   │   │           └── network-policy.yaml
│   │   └── kustomize/
│   │       ├── base/
│   │       │   ├── kustomization.yaml
│   │       │   ├── deployment.yaml
│   │       │   └── service.yaml
│   │       └── overlays/
│   │           ├── dev/
│   │           │   ├── kustomization.yaml
│   │           │   └── patch-replicas.yaml
│   │           ├── staging/
│   │           │   ├── kustomization.yaml
│   │           │   └── patch-replicas.yaml
│   │           └── prod/
│   │               ├── kustomization.yaml
│   │               ├── patch-replicas.yaml
│   │               └── patch-resources.yaml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── vpc.tf
│   │   ├── eks.tf
│   │   ├── rds.tf
│   │   ├── elasticache.tf
│   │   └── iam.tf
│   └── monitoring/
│       ├── prometheus/
│       │   └── prometheus.yml
│       └── grafana/
│           └── dashboards/
│               └── flight-system.json
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd-staging.yml
│       └── cd-production.yml
│
├── docs/
│   ├── architecture.md
│   ├── adr/
│   │   ├── 001-vertical-slice-cqrs.md
│   │   ├── 002-rag-pattern.md
│   │   └── 003-message-queue.md
│   └── runbook.md
│
├── .env.example
├── .gitignore
├── Makefile
└── README.md
```

---

## Propuesta de IA

### Nivel 1 — RAG Agent (ya implementado, mejorar)
- **Que hace:** Responde preguntas sobre vuelos usando datos reales de PostgreSQL y Redis
- **Mejora:** Agregar pgvector para busqueda semantica sobre destinos y preguntas frecuentes
- **Stack:** LangChain + Groq + pgvector

### Nivel 2 — Prediccion de Demanda
- **Que hace:** Predice la demanda futura por destino basado en historico de reservas
- **Input:** Datos historicos de bookings (destino, fecha, volumen, precio)
- **Output:** Score de demanda por destino + sugerencia de precio
- **Stack:** Datos de PostgreSQL procesados por el LLM con contexto enriquecido
- **Integracion:** Endpoint `POST /api/v1/ai/predict-demand` que alimenta al LLM con tendencias calculadas en Redis

### Nivel 3 — Asistente Conversacional Avanzado
- **Que hace:** Chat que puede ejecutar acciones (buscar vuelos, crear reservas, consultar stats)
- **Stack:** LangChain Agent con tool calling — el LLM decide que tools usar
- **Tools:** buscar_vuelo, crear_reserva, consultar_stats, consultar_impuestos
- **Integracion:** El agente tiene acceso a los commands y queries existentes via tools

### Nivel 4 — Analisis de Sentimiento y Recomendaciones
- **Que hace:** Analiza patrones de reserva para recomendar destinos y detectar tendencias
- **Input:** Historico de reservas + popularidad de destinos desde Redis
- **Output:** Recomendaciones personalizadas + alertas de tendencias
- **Stack:** LLM con prompts especializados + datos agregados de Redis

---

## Cronograma por Fases

### Fase 1 — Reestructuracion del Backend (Semana 1-2)

| Tarea | Descripcion |
|-------|-------------|
| Reorganizar carpetas | Mover a estructura `backend/` con nueva organizacion |
| Alembic | Reemplazar `create_all()` por migraciones |
| Auth feature | Crear slice `auth/` con JWT (register, login, me) |
| Error handling | Crear `shared/exceptions.py` con exception handlers centralizados |
| Middleware | CORS, rate limiting, logging estructurado |
| Stats feature | Crear slice `stats/` con queries a Redis para reportes |
| Linting | Configurar ruff + mypy en `pyproject.toml` |

### Fase 2 — Tests y Calidad (Semana 2-3)

| Tarea | Descripcion |
|-------|-------------|
| Tests unitarios | Tests para cada command y query de cada feature |
| Tests de integracion | Tests del flujo completo con DB real |
| Tests de schemas | Validar todas las reglas de Pydantic |
| Coverage | Configurar pytest-cov, objetivo >80% |
| CI pipeline lint | Agregar ruff + mypy al pipeline de GitHub Actions |
| CI pipeline security | Agregar bandit para analisis de seguridad |

### Fase 3 — Frontend React (Semana 3-5)

| Tarea | Descripcion |
|-------|-------------|
| Scaffolding | Crear proyecto con Vite + React + TypeScript |
| Auth pages | Login y registro conectados al backend |
| Dashboard | Vista principal con stats de Redis |
| Flights page | CRUD de destinos y vuelos |
| Bookings page | Formulario de reserva con calculo de precio en tiempo real |
| Stats page | Graficas de recaudo, destino preferido, infantes |
| AI Chat page | Chat con el agente RAG |
| Dockerfile frontend | Multi-stage build con nginx |

### Fase 4 — Docker y Compose (Semana 5-6)

| Tarea | Descripcion |
|-------|-------------|
| Dockerfile backend | Optimizar multi-stage build |
| Dockerfile frontend | Build React + serve con nginx |
| docker-compose.yml | Orquestar: api, worker, frontend, db, redis, rabbitmq |
| docker-compose.dev.yml | Override para desarrollo con hot-reload |
| docker-compose.monitoring.yml | Prometheus + Grafana |
| .env.example | Documentar todas las variables |
| Makefile | Comandos rapidos: make dev, make test, make build |

### Fase 5 — Kubernetes + Helm + Kustomize (Semana 6-8)

| Tarea | Descripcion |
|-------|-------------|
| Helm Chart | Templates para api, worker, frontend |
| Deployments | Con resource requests/limits, probes, replicas |
| Services | ClusterIP para internos, LoadBalancer/Ingress para externos |
| Ingress | Nginx ingress controller con TLS |
| ConfigMap + Secret | Variables por ambiente |
| HPA | Autoescalado por CPU y memoria |
| Network Policies | Restringir comunicacion entre pods |
| Kustomize base | Manifiestos base reutilizables |
| Kustomize overlays | Configuracion para dev, staging, prod |
| Kustomize patches | Replicas, resources, variables por ambiente |

### Fase 6 — IA y Agente Avanzado (Semana 8-9)

| Tarea | Descripcion |
|-------|-------------|
| pgvector | Habilitar extension en PostgreSQL para busqueda semantica |
| Embeddings | Generar embeddings de destinos y preguntas frecuentes |
| RAG mejorado | Busqueda semantica + datos de mercado + stats |
| Prediccion de demanda | Endpoint que analiza tendencias con contexto del LLM |
| Tool calling | Agente que puede ejecutar acciones via LangChain tools |
| Tests de IA | Tests con respuestas mockeadas del LLM |

### Fase 7 — Message Queue Avanzado (Semana 9-10)

| Tarea | Descripcion |
|-------|-------------|
| Nuevas tasks Celery | Notificaciones, calculo de reportes, alimentar datos para IA |
| Dead letter queue | Manejo de mensajes fallidos en RabbitMQ |
| Task monitoring | Flower para monitorear workers de Celery |
| Retry policies | Politicas de reintento diferenciadas por tipo de tarea |
| Event sourcing basico | Log de eventos de reservas para auditoria |

### Fase 8 — Observabilidad (Semana 10-11)

| Tarea | Descripcion |
|-------|-------------|
| Prometheus | Metricas de FastAPI (requests, latencia, errores) |
| Grafana dashboards | Dashboard de la aplicacion + dashboard de infra |
| OpenTelemetry | Tracing distribuido entre API y Worker |
| Alertas | Reglas en Prometheus para errores criticos |
| Health endpoints | Readiness y liveness probes mejorados |
| Logging JSON | Logging estructurado con correlation IDs |

### Fase 9 — Terraform + CI/CD Completo (Semana 11-13)

| Tarea | Descripcion |
|-------|-------------|
| Terraform VPC | Red en AWS |
| Terraform EKS | Cluster de Kubernetes |
| Terraform RDS | PostgreSQL managed |
| Terraform ElastiCache | Redis managed |
| Terraform IAM | Roles y politicas |
| CI pipeline | lint → security → test → coverage → build |
| CD staging | Deploy automatico a staging en push a develop |
| CD production | Deploy a produccion con aprobacion manual en push a main |
| Rollback | Estrategia de rollback documentada |

### Fase 10 — Deploy Publico y Documentacion (Semana 13-14)

| Tarea | Descripcion |
|-------|-------------|
| Deploy publico | Desplegar en Railway/Fly.io/AWS con URL publica |
| README profesional | Actualizar con screenshots, badges, demo URL |
| Architecture doc | Diagrama C4 de la arquitectura |
| ADRs | Documentar decisiones arquitectonicas clave |
| Runbook | Guia de operaciones para el sistema |
| LICENSE | MIT o Apache 2.0 |
| CONTRIBUTING.md | Guia de contribucion |

---

## Resumen Visual del Cronograma

```
Semana:  1   2   3   4   5   6   7   8   9  10  11  12  13  14
         ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
Fase 1:  ████████                                Backend
Fase 2:      ████████                            Tests
Fase 3:          ████████████                    Frontend React
Fase 4:                  ████████                Docker
Fase 5:                      ████████████        K8s + Helm + Kustomize
Fase 6:                              ████████    IA Avanzada
Fase 7:                                  ████████  Message Queue
Fase 8:                                      ████████  Observabilidad
Fase 9:                                          ████████████  Terraform + CI/CD
Fase 10:                                                 ████████  Deploy + Docs
```

---

## Resultado Esperado

Al completar las 10 fases, el proyecto demostrara:

| Area | Que demuestra |
|------|---------------|
| **Backend Python** | FastAPI + SQLAlchemy + Alembic + JWT + Pydantic v2 + CQRS |
| **Frontend React** | TypeScript + Vite + Zustand + Tailwind + componentes reutilizables |
| **DevOps** | Docker + Compose + K8s + Helm + Kustomize + Terraform |
| **CI/CD** | Pipeline completo con lint, security, test, build, deploy multi-ambiente |
| **IA** | RAG + pgvector + prediccion de demanda + agente con tool calling |
| **Message Queue** | RabbitMQ + Celery + dead letter + monitoring |
| **Observabilidad** | Prometheus + Grafana + OpenTelemetry + alertas |

**Rol objetivo alcanzable:** Junior+ / Mid-level Backend + DevOps Engineer
