# Flight Reservation System MVP

## Arquitectura
- **Backend:** FastAPI (Vertical Slices + CQRS).
- **Asincronía:** RabbitMQ + Celery para reportes y contabilidad de dulces.
- **IA:** Agente RAG con LangChain para sugerencia de precios.
- **Infra:** Docker Multi-stage y Kubernetes (Helm).

## Cómo ejecutar localmente
1. Clonar el repositorio.
2. Crear un archivo `.env` con `DATABASE_URL` y `OPENAI_API_KEY`.
3. Ejecutar `docker-compose up --build`.
4. Acceder a `http://localhost:8000/docs` para la documentación interactiva.

## Monitoreo
- **Métricas:** Los pods de K8s están anotados para ser scrapeados por **Prometheus**.
- **Dashboard:** Se incluye un template de **Grafana** en `infra/monitoring/` para visualizar:
  - Total Recaudado (vía Redis).
  - Uso de CPU/RAM por pod.
  - Tasa de error de reservas.