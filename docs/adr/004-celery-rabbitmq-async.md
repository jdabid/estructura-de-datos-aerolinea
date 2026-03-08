# ADR-004: Procesamiento Asíncrono con Celery y RabbitMQ

**Fecha:** 2025-01-20
**Estado:** Aceptado

## Contexto

Ciertas operaciones post-reserva no necesitan ejecutarse de forma síncrona:
actualización de estadísticas en Redis, registro de logs, cálculo de métricas
agregadas y potenciales notificaciones. Ejecutar estas tareas dentro del request
HTTP aumenta la latencia innecesariamente.

## Decisión

Se adopta **Celery 5** como task queue con **RabbitMQ 3** como message broker:
- Los commands despachan eventos vía `task.delay(json.dumps(payload))`
- El worker Celery (`src/worker/`) procesa tareas en segundo plano
- Redis se usa como backend de resultados y almacén de contadores

Estructura:
```
src/worker/
├── celery_app.py   # Configuración de Celery
└── tasks.py        # Definición de tareas asíncronas
```

Las tareas incluyen: actualizar contadores de reservas, registrar logs de
actividad, calcular estadísticas del dashboard.

## Consecuencias

**Positivas:**
- Respuestas HTTP rápidas al desacoplar operaciones secundarias
- RabbitMQ garantiza entrega de mensajes (no se pierden tareas)
- Escalabilidad horizontal: se pueden agregar más workers según demanda
- Reintentos automáticos en caso de fallo

**Negativas:**
- Complejidad operacional: tres servicios adicionales (RabbitMQ, Celery, Redis)
- Debugging más complejo en flujos asíncronos
- Eventual consistency: las estadísticas pueden tener delay de segundos
- Requiere monitoreo adicional (Flower o similar) para visibilidad de tareas
