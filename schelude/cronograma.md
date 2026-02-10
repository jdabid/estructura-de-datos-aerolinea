### Cronograma de Desarrollo (6 Semanas - MVP)

| Fase | Semana | Actividades Principales | Entregables |
| :--- | :--- | :--- | :--- |
| **1. Base e Infra** | 1 | Configuración de repo, CI/CD inicial, Docker Multi-stage y setup de K8s con Helm. | Entorno local con `docker-compose` y esqueleto de K8s. |
| **2. Gestión de Vuelos** | 2 | Implementación del slice `flights`. Modelado en PostgreSQL y API base de FastAPI. | CRUD de vuelos y configuración de impuestos por destino. |
| **3. Reservas y CQRS** | 3 | Implementación del slice `bookings`. Lógica de Commands para reservas y Queries para lectura. | Sistema de reservas con validación de mascotas y descuentos. |
| **4. Eventos y Workers** | 4 | Integración de RabbitMQ + Celery. Procesamiento asíncrono de reportes y lógica de dulces. | Registro automático de dulces y actualización de estadísticas en Redis. |
| **5. Inteligencia Artificial** | 5 | Implementación de Agente IA con LangChain (RAG) para consultas y precios dinámicos. | Chatbot funcional y sugerencias de precios basadas en demanda. |
| **6. QA y Despliegue** | 6 | Pruebas de integración, optimización de imágenes y despliegue final en producción. | Aplicación productiva con monitoreo básico y documentación. |

---
