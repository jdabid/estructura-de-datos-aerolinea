# Cronograma Scrum: Flight Reservation System

> Metodologia Scrum adaptada para desarrollador individual.
> Sprints de 2 semanas | 7 Sprints | 14 semanas totales.

---

## Roles Scrum (Adaptados)

| Rol | Responsable |
|-----|-------------|
| Product Owner | Tu (defines prioridades del portafolio) |
| Scrum Master | Tu (facilitas tu propio proceso) |
| Development Team | Tu (ejecutas el trabajo) |

---

## Product Backlog (Epicas)

| ID | Epica | Prioridad | Story Points Totales |
|----|-------|-----------|---------------------|
| E1 | Reestructuracion Backend + Auth | Critica | 34 |
| E2 | Testing y Calidad de Codigo | Critica | 21 |
| E3 | Frontend React | Alta | 34 |
| E4 | Docker y Compose Profesional | Alta | 13 |
| E5 | Kubernetes + Helm + Kustomize | Alta | 34 |
| E6 | IA y Agente Avanzado | Media | 21 |
| E7 | Message Queue Avanzado | Media | 13 |
| E8 | Observabilidad | Media | 21 |
| E9 | Terraform + CI/CD Completo | Alta | 21 |
| E10 | Deploy Publico + Documentacion | Critica | 13 |

**Velocidad estimada:** 30-35 story points por sprint.

---

## Sprint 1 — Fundamentos Backend

**Sprint Goal:** Reestructurar el backend con migraciones, autenticacion y manejo de errores profesional.

**Duracion:** Semana 1-2

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-01 | Como developer, quiero reorganizar las carpetas del proyecto en `backend/` para separar responsabilidades | 3 | Estructura `backend/src/` creada, imports actualizados, app arranca sin errores |
| US-02 | Como developer, quiero migraciones con Alembic para gestionar cambios de DB profesionalmente | 5 | Alembic configurado, migracion inicial generada, `create_all()` eliminado de main.py |
| US-03 | Como usuario, quiero registrarme y hacer login para acceder al sistema de forma segura | 8 | Endpoints `/auth/register`, `/auth/login`, `/auth/me` funcionando con JWT |
| US-04 | Como developer, quiero un sistema de excepciones centralizado para manejar errores de forma consistente | 5 | `shared/exceptions.py` con custom exceptions, handlers registrados en FastAPI |
| US-05 | Como developer, quiero middleware de CORS y rate limiting para proteger la API | 3 | CORS configurado, rate limiting en endpoints sensibles |
| US-06 | Como developer, quiero configurar ruff y mypy para mantener calidad de codigo | 3 | `pyproject.toml` configurado, ruff y mypy pasan sin errores |
| US-07 | Como developer, quiero un feature `stats/` con queries a Redis para exponer reportes via API | 5 | Endpoints GET para total recaudo, destino preferido, infantes, costo dulces |

**Total SP:** 32

### Ceremonies Sprint 1

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Revisar stories, definir tareas, estimar |
| Daily Standup | Cada dia | 10 min | Que hice ayer, que hare hoy, bloqueos (escribir en un diario) |
| Sprint Review | Dia 14 | 30 min | Demo: levantar la app, mostrar auth + migraciones + stats |
| Sprint Retrospective | Dia 14 | 20 min | Que salio bien, que mejorar, que probar diferente |

### Definition of Done — Sprint 1
- [ ] Codigo funcional y sin errores de linting
- [ ] Migraciones de Alembic corren limpiamente
- [ ] JWT auth protege endpoints existentes
- [ ] `docker compose up --build` arranca sin errores
- [ ] Endpoints de stats retornan datos de Redis

---

## Sprint 2 — Tests + Inicio Frontend

**Sprint Goal:** Alcanzar >80% de coverage en backend y crear el scaffolding del frontend con auth.

**Duracion:** Semana 3-4

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-08 | Como developer, quiero tests unitarios para flights commands y queries | 5 | Tests para create_destination, create_flight, get_flights, get_destinations |
| US-09 | Como developer, quiero tests unitarios para bookings commands y queries | 5 | Tests para create_booking (con promo, sin promo, pet validation, infant) |
| US-10 | Como developer, quiero tests para auth y schemas | 3 | Tests de register, login, token validation, schema validators |
| US-11 | Como developer, quiero coverage >80% con reporte en CI | 3 | pytest-cov configurado, coverage report generado, threshold en pipeline |
| US-12 | Como usuario, quiero una app React donde pueda ver la pagina de login | 5 | Proyecto Vite + React + TS creado, pagina de login funcional |
| US-13 | Como usuario, quiero hacer login en el frontend y mantener mi sesion | 5 | Auth store con Zustand, token guardado, redireccion post-login |
| US-14 | Como usuario, quiero ver un dashboard con estadisticas generales | 5 | Pagina dashboard con cards de stats consumiendo API |
| US-15 | Como developer, quiero agregar bandit al pipeline CI para detectar vulnerabilidades | 2 | bandit corre en GitHub Actions, sin vulnerabilidades criticas |

**Total SP:** 33

### Ceremonies Sprint 2

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Revisar backlog, ajustar velocidad segun Sprint 1 |
| Daily Standup | Cada dia | 10 min | Registro diario de progreso |
| Sprint Review | Dia 14 | 30 min | Demo: correr tests con coverage, mostrar frontend login + dashboard |
| Sprint Retrospective | Dia 14 | 20 min | Evaluar velocidad real vs estimada |

### Definition of Done — Sprint 2
- [ ] Coverage >80% con reporte visible
- [ ] Frontend arranca con Vite, login funcional contra backend
- [ ] Dashboard muestra stats reales del backend
- [ ] Pipeline CI incluye lint + security + tests

---

## Sprint 3 — Frontend Completo

**Sprint Goal:** Completar todas las paginas del frontend con funcionalidad real.

**Duracion:** Semana 5-6

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-16 | Como usuario, quiero ver la lista de destinos y vuelos disponibles | 5 | Pagina Flights con tabla de destinos y vuelos, datos del API |
| US-17 | Como admin, quiero crear destinos y vuelos desde el frontend | 5 | Formularios con validacion, feedback de exito/error |
| US-18 | Como usuario, quiero crear una reserva y ver el precio calculado en tiempo real | 8 | Formulario BookingForm, preview de precio (promo + tax), confirmacion |
| US-19 | Como usuario, quiero ver el historial de reservas | 3 | Pagina Bookings con tabla de reservas, filtros basicos |
| US-20 | Como usuario, quiero ver graficas de estadisticas de la aerolinea | 5 | Pagina Stats con graficas de recaudo, destino preferido, infantes |
| US-21 | Como usuario, quiero chatear con el agente de IA sobre vuelos | 5 | Pagina AiChat con ventana de chat, envio de mensajes, respuestas del agente |
| US-22 | Como developer, quiero un Dockerfile para el frontend con nginx | 3 | Multi-stage build: Vite build + nginx serve, imagen funcional |

**Total SP:** 34

### Ceremonies Sprint 3

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Priorizar paginas por impacto visual en portafolio |
| Daily Standup | Cada dia | 10 min | Registro diario |
| Sprint Review | Dia 14 | 30 min | Demo completa: flujo usuario login → buscar vuelo → reservar → ver stats → chat IA |
| Sprint Retrospective | Dia 14 | 20 min | Evaluar deuda tecnica acumulada |

### Definition of Done — Sprint 3
- [ ] Todas las paginas funcionales y conectadas al backend
- [ ] Formularios con validacion del lado del cliente
- [ ] Dockerfile frontend genera imagen funcional
- [ ] Navegacion completa entre paginas

---

## Sprint 4 — Docker Profesional + Kubernetes Base

**Sprint Goal:** Contenedorizacion profesional y despliegue base en Kubernetes con Helm.

**Duracion:** Semana 7-8

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-23 | Como developer, quiero docker-compose.yml con todos los servicios (api, worker, frontend, db, redis, rabbitmq) | 5 | Compose levanta los 6 servicios, healthchecks, red interna |
| US-24 | Como developer, quiero docker-compose.dev.yml con hot-reload para desarrollo | 3 | Override con volumes para backend y frontend, recarga automatica |
| US-25 | Como developer, quiero un Makefile con comandos rapidos | 2 | `make dev`, `make test`, `make build`, `make clean` |
| US-26 | Como DevOps, quiero Helm Chart con templates para api, worker y frontend | 8 | Chart.yaml, values.yaml, templates de deployment, service, configmap, secret |
| US-27 | Como DevOps, quiero HPA para autoescalado del API y worker | 3 | HPA configurado: min 2, max 10, target CPU 70% |
| US-28 | Como DevOps, quiero ingress controller con TLS configurado en Helm | 5 | Ingress template con annotations para nginx, TLS placeholder |
| US-29 | Como DevOps, quiero network policies para restringir comunicacion entre pods | 3 | Solo api puede hablar con db, solo worker con redis y rabbitmq |
| US-30 | Como DevOps, quiero resource requests y limits reales en los deployments | 3 | CPU/memory requests y limits definidos por servicio en values.yaml |

**Total SP:** 32

### Ceremonies Sprint 4

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Definir valores de resources basados en observacion de compose |
| Daily Standup | Cada dia | 10 min | Registro diario |
| Sprint Review | Dia 14 | 30 min | Demo: `docker compose up`, `helm template`, `helm install --dry-run` |
| Sprint Retrospective | Dia 14 | 20 min | Evaluar complejidad real de K8s vs estimada |

### Definition of Done — Sprint 4
- [ ] `docker compose up --build` levanta todo el stack (api + frontend + infra)
- [ ] `docker compose -f docker-compose.dev.yml up` funciona con hot-reload
- [ ] `helm template` genera manifiestos validos
- [ ] Network policies y HPA definidos

---

## Sprint 5 — Kustomize + IA Avanzada

**Sprint Goal:** Configurar ambientes con Kustomize y mejorar el agente de IA con RAG avanzado.

**Duracion:** Semana 9-10

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-31 | Como DevOps, quiero Kustomize base con manifiestos reutilizables | 5 | `base/` con deployment, service, kustomization.yaml |
| US-32 | Como DevOps, quiero overlays de Kustomize para dev, staging y prod | 5 | Cada overlay tiene patches de replicas, resources y variables |
| US-33 | Como DevOps, quiero que `kustomize build` genere manifiestos validos por ambiente | 3 | `kustomize build overlays/dev`, `staging`, `prod` sin errores |
| US-34 | Como developer, quiero habilitar pgvector en PostgreSQL para busqueda semantica | 5 | Extension pgvector activa, tabla de embeddings creada con Alembic |
| US-35 | Como usuario, quiero que el agente IA busque destinos semanticamente | 5 | Busqueda por similitud: "playa calida" encuentra "Cartagena", "San Andres" |
| US-36 | Como usuario, quiero que el agente IA prediga demanda por destino | 5 | Endpoint `/ai/predict-demand` retorna score + sugerencia de precio |
| US-37 | Como developer, quiero que el agente use tool calling para ejecutar acciones | 5 | LangChain Agent con tools: buscar_vuelo, consultar_stats, consultar_impuestos |

**Total SP:** 33

### Ceremonies Sprint 5

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Balancear trabajo DevOps + IA |
| Daily Standup | Cada dia | 10 min | Registro diario |
| Sprint Review | Dia 14 | 30 min | Demo: `kustomize build` por ambiente + chat IA con busqueda semantica |
| Sprint Retrospective | Dia 14 | 20 min | Evaluar si IA agrega valor real al portafolio |

### Definition of Done — Sprint 5
- [ ] 3 overlays de Kustomize generan manifiestos diferenciados
- [ ] pgvector funcional con embeddings de destinos
- [ ] Agente IA responde con contexto semantico
- [ ] Endpoint de prediccion de demanda funcional

---

## Sprint 6 — Message Queue + Observabilidad

**Sprint Goal:** Robustecer el procesamiento asincrono y agregar observabilidad completa.

**Duracion:** Semana 11-12

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-38 | Como developer, quiero dead letter queue para mensajes fallidos | 3 | RabbitMQ DLQ configurada, mensajes fallidos llegan a la cola muerta |
| US-39 | Como developer, quiero Flower para monitorear workers de Celery | 3 | Flower accesible en puerto 5555, muestra tasks activas y completadas |
| US-40 | Como developer, quiero nuevas tasks: notificaciones y alimentar datos para IA | 5 | Tasks creadas con retry policies diferenciadas |
| US-41 | Como developer, quiero event log de reservas para auditoria | 3 | Cada booking genera un evento inmutable en Redis list |
| US-42 | Como DevOps, quiero metricas de Prometheus en FastAPI | 5 | prometheus-fastapi-instrumentator expone /metrics con requests, latencia, errores |
| US-43 | Como DevOps, quiero dashboards de Grafana pre-configurados | 5 | docker-compose.monitoring.yml con Prometheus + Grafana + dashboard JSON |
| US-44 | Como DevOps, quiero tracing distribuido con OpenTelemetry | 5 | Traces entre API request → Celery task → Redis visible en Jaeger |
| US-45 | Como DevOps, quiero logging estructurado en JSON con correlation IDs | 3 | Todos los logs en formato JSON, cada request tiene un trace_id |

**Total SP:** 32

### Ceremonies Sprint 6

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Priorizar observabilidad sobre message queue si hay conflicto |
| Daily Standup | Cada dia | 10 min | Registro diario |
| Sprint Review | Dia 14 | 30 min | Demo: dashboard Grafana en vivo, Flower con tasks, tracing en Jaeger |
| Sprint Retrospective | Dia 14 | 20 min | Evaluar complejidad de observabilidad |

### Definition of Done — Sprint 6
- [ ] Prometheus scrapeando metricas de la API
- [ ] Grafana con dashboard funcional
- [ ] Flower mostrando workers activos
- [ ] Logs en JSON con correlation IDs
- [ ] DLQ capturando mensajes fallidos

---

## Sprint 7 — Terraform + CI/CD + Deploy Publico

**Sprint Goal:** Infraestructura como codigo, pipeline completo y deploy publico funcional.

**Duracion:** Semana 13-14

| ID | User Story | SP | Criterio de Aceptacion |
|----|------------|----|-----------------------|
| US-46 | Como DevOps, quiero Terraform para provisionar VPC + EKS en AWS | 5 | `terraform plan` genera plan valido para VPC y cluster EKS |
| US-47 | Como DevOps, quiero Terraform para RDS (PostgreSQL) y ElastiCache (Redis) | 5 | Modulos de RDS y ElastiCache definidos con variables |
| US-48 | Como DevOps, quiero Terraform con IAM roles y politicas | 3 | Roles para EKS, RDS access, policies least-privilege |
| US-49 | Como DevOps, quiero pipeline CI completo: lint → security → test → build | 5 | GitHub Actions con 4 jobs, falla si lint/security/test fallan |
| US-50 | Como DevOps, quiero pipeline CD con deploy a staging automatico y prod con aprobacion | 5 | cd-staging.yml auto en push a develop, cd-production.yml con manual approval |
| US-51 | Como developer, quiero deploy publico funcional con URL accesible | 5 | App desplegada en Railway/Fly.io/AWS, URL publica en README |
| US-52 | Como developer, quiero documentacion profesional: ADRs, diagrama C4, runbook | 3 | docs/ con architecture.md, 3 ADRs, runbook.md |
| US-53 | Como developer, quiero README actualizado con badges, screenshots y demo URL | 2 | README con CI badge, coverage badge, screenshots, link a demo |

**Total SP:** 33

### Ceremonies Sprint 7

| Ceremonia | Cuando | Duracion | Que hacer |
|-----------|--------|----------|-----------|
| Sprint Planning | Dia 1 | 1 hora | Priorizar deploy publico como entregable critico |
| Daily Standup | Cada dia | 10 min | Registro diario |
| Sprint Review | Dia 14 | 1 hora | Demo FINAL: flujo completo end-to-end en URL publica |
| Sprint Retrospective | Dia 14 | 30 min | Retrospectiva general de los 7 sprints |

### Definition of Done — Sprint 7
- [ ] `terraform plan` exitoso (no requiere `apply` real si no hay cuenta AWS)
- [ ] Pipeline CI/CD completo en GitHub Actions
- [ ] App desplegada con URL publica
- [ ] README profesional con badges y demo
- [ ] Documentacion completa en `docs/`

---

## Burndown Chart Proyectado

```
Story Points
Restantes
  225 |*
      |  *
  200 |    *
      |      *
  175 |        *
      |          *
  150 |            *
      |              *
  125 |                *
      |                  *
  100 |                    *
      |                      *
   75 |                        *
      |                          *
   50 |                            *
      |                              *
   25 |                                *
      |                                  *
    0 |____________________________________*
      S1    S2    S3    S4    S5    S6    S7
```

| Sprint | SP Planificados | SP Acumulados | Restantes |
|--------|----------------|---------------|-----------|
| S1 | 32 | 32 | 193 |
| S2 | 33 | 65 | 160 |
| S3 | 34 | 99 | 126 |
| S4 | 32 | 131 | 94 |
| S5 | 33 | 164 | 61 |
| S6 | 32 | 196 | 29 |
| S7 | 33 | 229 | 0 |

**Total:** 229 Story Points | 53 User Stories | 7 Sprints | 14 Semanas

---

## Artefactos Scrum

### Product Backlog
- Documento vivo con todas las user stories priorizadas (este documento)
- Repriorizar al inicio de cada sprint segun aprendizajes

### Sprint Backlog
- Al inicio de cada sprint, tomar las stories asignadas y descomponerlas en tareas tecnicas
- Usar GitHub Projects o un Kanban simple (To Do, In Progress, Done)

### Incremento
- Al final de cada sprint, un incremento funcional y desplegable
- Cada sprint produce una version que se puede mostrar en el portafolio

---

## Herramientas Sugeridas para Gestionar el Scrum

| Herramienta | Uso |
|-------------|-----|
| **GitHub Projects** | Kanban board con las user stories |
| **GitHub Issues** | Cada user story es un issue con labels (epica, sprint, prioridad) |
| **GitHub Milestones** | Cada sprint es un milestone |
| **Diario personal** | Daily standups escritos (que hice, que hare, bloqueos) |
| **README de sprint** | Al final de cada sprint, escribir un mini post-mortem |

---

## Definition of Done (Global)

Cada user story esta "Done" cuando cumple:

- [ ] Codigo funcional sin errores
- [ ] Ruff y mypy pasan sin warnings
- [ ] Tests escritos y pasando
- [ ] Documentacion actualizada si aplica
- [ ] Commit con mensaje descriptivo
- [ ] PR creado (aunque sea self-review, practica el flujo)

---

## Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|-------------|---------|------------|
| Subestimar complejidad de K8s | Alta | Alto | Empezar con minikube, no intentar cluster real hasta Sprint 7 |
| Perder motivacion en Sprints largos | Media | Alto | Celebrar cada Sprint Review como un logro, publicar progreso en LinkedIn |
| Bloqueo por falta de cuenta AWS | Media | Medio | Terraform solo con `plan`, deploy real en Railway/Fly.io (gratis) |
| Scope creep en IA | Media | Medio | Limitar IA a lo definido, no agregar features no planificadas |
| pgvector complejo de configurar | Baja | Bajo | Fallback: usar busqueda por keywords en lugar de embeddings |
