# ADR-001: Vertical Slice Architecture

**Fecha:** 2025-01-15
**Estado:** Aceptado

## Contexto

El sistema de reservas de vuelos necesita una arquitectura que permita escalar el desarrollo
por funcionalidades independientes, facilitando que cada feature (vuelos, reservas, IA) evolucione
sin acoplamientos innecesarios. La arquitectura tradicional en capas (controllers/services/repos)
genera dependencias transversales que dificultan cambios aislados.

## Decisión

Se adopta **Vertical Slice Architecture**, donde cada feature contiene todos sus componentes:
- `models.py` - Modelos SQLAlchemy
- `schemas.py` - Schemas Pydantic v2
- `commands.py` - Operaciones de escritura
- `queries.py` - Operaciones de lectura

Estructura resultante:
```
src/features/
├── flights/    (models, schemas, commands, queries)
├── bookings/   (models, schemas, commands, queries)
└── ai/         (agent, tools)
```

El código compartido (database, redis, métricas) se mantiene en `src/shared/`.

## Consecuencias

**Positivas:**
- Cada feature es autocontenida y se puede modificar sin afectar otras
- Facilita onboarding: un desarrollador trabaja en un directorio aislado
- Alineado con Domain-Driven Design a nivel táctico
- Simplifica testing por feature

**Negativas:**
- Posible duplicación de código entre slices (mitigado con `src/shared/`)
- Requiere disciplina para no crear dependencias cruzadas entre features
- Curva de aprendizaje para equipos acostumbrados a arquitectura en capas
