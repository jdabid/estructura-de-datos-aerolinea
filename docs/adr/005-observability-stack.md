# ADR-005: Stack de Observabilidad

**Fecha:** 2025-02-15
**Estado:** Aceptado

## Contexto

Un sistema distribuido con API, workers, base de datos, caché y message broker
requiere observabilidad integral para detectar problemas, analizar rendimiento
y responder a incidentes. Sin métricas, logs centralizados y trazas, diagnosticar
fallos en producción es inviable.

## Decisión

Se implementa el stack de observabilidad con tres pilares:

**Métricas:** Prometheus + Grafana
- Prometheus scraping de `/metrics` en la API (vía `prometheus-fastapi-instrumentator`)
- Dashboards Grafana para latencia, throughput, errores y saturación (RED/USE)

**Trazas:** Jaeger (OpenTelemetry)
- Tracing distribuido para seguir requests a través de API → Worker → DB
- Instrumentación automática con OpenTelemetry SDK

**Logs:** Logs estructurados JSON
- Formato JSON para facilitar ingesta en herramientas de log aggregation
- Correlation IDs para vincular logs con trazas

## Consecuencias

**Positivas:**
- Visibilidad completa del sistema (métricas, trazas, logs)
- Alertas proactivas antes de que los usuarios reporten problemas
- Facilita root cause analysis con trazas distribuidas
- Stack open-source sin costos de licencia

**Negativas:**
- Overhead de infraestructura: tres servicios adicionales en el cluster
- Consumo de recursos (CPU/RAM) por collectors y agents
- Requiere configuración y mantenimiento de dashboards y alertas
- Volumen de datos de observabilidad puede crecer significativamente
