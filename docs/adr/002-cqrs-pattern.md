# ADR-002: Patrón CQRS

**Fecha:** 2025-01-15
**Estado:** Aceptado

## Contexto

Las operaciones de lectura y escritura en el sistema tienen características distintas:
las lecturas son frecuentes y requieren baja latencia (consultas de vuelos, estadísticas),
mientras que las escrituras implican lógica de negocio compleja (crear reservas con cálculo
de precios, validación de mascotas, descuentos promocionales). Mezclar ambas en un solo
módulo dificulta la optimización independiente.

## Decisión

Se implementa **CQRS (Command Query Responsibility Segregation)** a nivel de código:
- **Commands** (`commands.py`): operaciones de escritura (crear, actualizar, eliminar)
- **Queries** (`queries.py`): operaciones de lectura (listar, buscar, filtrar)

Cada feature separa sus operaciones en estos dos módulos. Los commands pueden despachar
eventos asíncronos a Celery para procesamiento posterior (estadísticas, notificaciones).

Las queries pueden aprovechar Redis como caché para lecturas frecuentes.

## Consecuencias

**Positivas:**
- Separación clara de responsabilidades de lectura/escritura
- Permite optimizar queries con caché (Redis) sin afectar la lógica de escritura
- Los commands pueden emitir eventos para procesamiento asíncrono
- Facilita testing unitario al tener funciones con responsabilidad única

**Negativas:**
- Mayor cantidad de archivos por feature
- Para operaciones simples (CRUD básico) puede parecer sobreingeniería
- Eventual consistency entre comando ejecutado y query actualizada
