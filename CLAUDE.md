# Flight Reservation System - Claude Code Instructions

## Project Overview
Sistema de reservas de vuelos con FastAPI, PostgreSQL, Redis, RabbitMQ, Celery y agente de IA (LangChain + Groq).

## Architecture
- **Pattern**: Vertical Slice Architecture + CQRS
- **Each feature** has: `models.py`, `schemas.py`, `commands.py`, `queries.py`
- **API routes** live in `src/api/v1/`
- **Shared code** in `src/shared/` (database, redis)
- **Workers** in `src/worker/` (Celery tasks)

## Project Structure
```
src/
├── main.py                    # FastAPI entry point
├── api/v1/                    # Route handlers
│   ├── flights.py
│   ├── bookings.py
│   └── ai.py
├── features/                  # Vertical slices
│   ├── flights/               # models, schemas, commands, queries
│   ├── bookings/              # models, schemas, commands, queries
│   └── ai/                    # agent.py, tools.py
├── shared/
│   ├── database.py            # SQLAlchemy engine + session
│   └── redis_client.py        # Redis helpers
└── worker/
    ├── celery_app.py
    └── tasks.py
```

## Tech Stack
- Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0
- PostgreSQL 15, Redis 7, RabbitMQ 3, Celery 5
- LangChain + Groq (Llama 3.3 70B) for AI agent
- Docker multi-stage, Kubernetes + Helm, GitHub Actions

## Key Conventions
- All schemas use Pydantic v2 with `ConfigDict(from_attributes=True)`
- Validators use `@field_validator` (Pydantic v2 style)
- Commands = write operations, Queries = read operations (CQRS)
- DB sessions via FastAPI `Depends(get_db)` dependency injection
- Async events dispatched to Celery via `task.delay(json.dumps(payload))`
- Redis keys follow pattern: `stats:*` for counters, `logs:*` for lists
- AI tools use `@tool` decorator from LangChain
- Response language: Spanish

## Business Rules
- Promotion discount: 10% off `base_price` when `is_promotion=True`
- Tax: `tax_amount` added to price (per destination)
- Pets: rejected with 400 if destination `allows_pets=False`
- Infants (<12 years): automatic candy cost of 5.0 tracked in Redis
- Formula: `total = (base_price * 0.90 if promo else base_price) + tax_amount`

## Running the Project
```bash
docker compose up --build -d       # Start all services
docker compose ps                  # Check status
docker compose logs -f api         # API logs
docker compose logs -f worker      # Worker logs
```

## Testing
```bash
# Inside Docker (recommended)
docker compose exec api pytest tests/ -v --tb=short
# After tests, restart API to recreate tables
docker compose restart api
```

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection (default in docker-compose)
- `RABBITMQ_URL` - RabbitMQ connection (default in docker-compose)
- `REDIS_HOST` / `REDIS_PORT` - Redis connection
- `GROQ_API_KEY` - Required only for AI endpoints (from .env)

## Adding a New Feature (Vertical Slice)
1. Create `src/features/{name}/models.py` - SQLAlchemy models
2. Create `src/features/{name}/schemas.py` - Pydantic schemas
3. Create `src/features/{name}/commands.py` - Write operations
4. Create `src/features/{name}/queries.py` - Read operations
5. Create `src/api/v1/{name}.py` - FastAPI router
6. Register router in `src/main.py` with `app.include_router()`
7. Add tests in `tests/test_{name}.py`

## Git Workflow

### Branch Naming
```
{tipo}/{sprint}-{US-ID}-{descripcion-corta}
```
Tipos: `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `infra/`, `chore/`

Example: `feature/s1-US03-jwt-auth`

### Commit Convention (Conventional Commits)
```
{tipo}({scope}): {descripcion en imperativo}
```
- Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `chore`, `ci`, `perf`, `infra`
- Scopes: `flights`, `bookings`, `auth`, `ai`, `stats`, `worker`, `shared`, `api`, `docker`, `helm`, `k8s`, `kustomize`, `terraform`, `ci`, `frontend`, `tests`
- En espanol, minusculas, max 72 chars, sin punto final

Example: `feat(auth): agregar endpoint de registro con JWT`

### PR Title
```
[US-{ID}] {tipo}: {descripcion}
```
Example: `[US-03] feat: agregar autenticacion JWT`

### Available Skills
| Skill | File | Purpose |
|-------|------|---------|
| Start US | `start-user-story.md` | Iniciar una User Story (branch + setup) |
| Finish US | `finish-user-story.md` | Finalizar US (push + PR + merge) |
| Git Workflow | `git-workflow.md` | Convenciones de branch, commit y PR |
| New Feature | `new-feature.md` | Crear vertical slice completo |
| New Endpoint | `new-endpoint.md` | Agregar endpoint a feature existente |
| Run Tests | `run-tests.md` | Ejecutar y diagnosticar tests |
| Docker Ops | `docker-ops.md` | Gestionar servicios Docker |
| New Celery Task | `new-celery-task.md` | Crear tarea asincrona |
| AI Tool | `ai-tool.md` | Agregar herramienta LangChain RAG |
