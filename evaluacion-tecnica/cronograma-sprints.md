# Cronograma de Sprints — Tracking en Tiempo Real

> Este documento se actualiza automaticamente cada vez que se finaliza una User Story.
> Ultima actualizacion: 2026-03-07

---

## Resumen General

| Metrica | Valor |
|---------|-------|
| Total User Stories | 53 |
| Completadas | 45 |
| En progreso | 0 |
| Pendientes | 8 |
| Story Points totales | 229 |
| Story Points completados | 196 |
| Story Points restantes | 33 |
| Velocidad actual | 32 SP (Sprint 1), 33 SP (Sprint 2), 34 SP (Sprint 3), 32 SP (Sprint 4), 33 SP (Sprint 5), 32 SP (Sprint 6) |
| Sprint actual | Sprint 6 COMPLETADO |

### Progreso Global

```
Completado: [##################################________] 86%  (196/229 SP)
```

---

## Sprint 1 — Fundamentos Backend

**Sprint Goal:** Reestructurar el backend con migraciones, autenticacion y manejo de errores profesional.
**Duracion:** Semana 1-2
**Estado:** COMPLETADO
**SP Completados:** 32/32

```
Sprint 1: [######################################] 100%  (32/32 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-01 | Reorganizar carpetas del proyecto en `backend/` | 3 | DONE | `feature/s1-US01-reorganizar-carpetas` | [#13](https://github.com/jdabid/flight-reservation-system/pull/13) | 2026-03-06 |
| US-02 | Migraciones con Alembic | 5 | DONE | `feature/s1-US02-alembic-migraciones` | [#14](https://github.com/jdabid/flight-reservation-system/pull/14) | 2026-03-06 |
| US-03 | Registro y login con JWT | 8 | DONE | `feature/s1-US03-jwt-auth` | [#15](https://github.com/jdabid/flight-reservation-system/pull/15) | 2026-03-06 |
| US-04 | Sistema de excepciones centralizado | 5 | DONE | `feature/s1-US04-excepciones-centralizadas` | [#17](https://github.com/jdabid/flight-reservation-system/pull/17) | 2026-03-06 |
| US-05 | Middleware CORS y rate limiting | 3 | DONE | `feature/s1-US05-cors-rate-limiting` | [#18](https://github.com/jdabid/flight-reservation-system/pull/18) | 2026-03-06 |
| US-06 | Configurar ruff y mypy | 3 | DONE | `feature/s1-US06-ruff-mypy` | [#16](https://github.com/jdabid/flight-reservation-system/pull/16) | 2026-03-06 |
| US-07 | Feature stats/ con queries a Redis | 5 | DONE | `feature/s1-US07-stats-feature` | [#19](https://github.com/jdabid/flight-reservation-system/pull/19) | 2026-03-06 |

### Notas del Sprint 1
- US-01, US-02, US-03 completadas en batch 1 (US-02/03 en paralelo con Agents worktree)
- US-04, US-05, US-06, US-07 completadas en batch 2 (las 4 en paralelo con Agents worktree)
- US-03 requirio rebase por conflicto en main.py con US-02 (resuelto)
- US-05 y US-07 requirieron rebase por conflictos en main.py (resueltos)
- Sprint 1 completado en un solo dia

---

## Sprint 2 — Tests + Inicio Frontend

**Sprint Goal:** Alcanzar >80% de coverage en backend y crear el scaffolding del frontend con auth.
**Duracion:** Semana 3-4
**Estado:** COMPLETADO
**SP Completados:** 33/33

```
Sprint 2: [######################################] 100%  (33/33 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-08 | Tests unitarios para flights commands y queries | 5 | DONE | `feature/s2-US08-tests-flights` | [#20](https://github.com/jdabid/flight-reservation-system/pull/20) | 2026-03-06 |
| US-09 | Tests unitarios para bookings commands y queries | 5 | DONE | `feature/s2-US09-tests-bookings` | [#21](https://github.com/jdabid/flight-reservation-system/pull/21) | 2026-03-06 |
| US-10 | Tests para auth y schemas | 3 | DONE | `feature/s2-US10-tests-auth` | [#22](https://github.com/jdabid/flight-reservation-system/pull/22) | 2026-03-06 |
| US-11 | Coverage >80% con reporte en CI | 3 | DONE | `feature/s2-US11-coverage-ci` | [#23](https://github.com/jdabid/flight-reservation-system/pull/23) | 2026-03-06 |
| US-12 | App React con pagina de login | 5 | DONE | `feature/s2-US12-US13-frontend-auth` | [#24](https://github.com/jdabid/flight-reservation-system/pull/24) | 2026-03-06 |
| US-13 | Login en frontend y mantener sesion | 5 | DONE | `feature/s2-US12-US13-frontend-auth` | [#24](https://github.com/jdabid/flight-reservation-system/pull/24) | 2026-03-06 |
| US-14 | Dashboard con estadisticas generales | 5 | DONE | `feature/s2-US14-dashboard-stats` | [#26](https://github.com/jdabid/flight-reservation-system/pull/26) | 2026-03-06 |
| US-15 | Agregar bandit al pipeline CI | 2 | DONE | `feature/s2-US15-bandit-ci` | [#25](https://github.com/jdabid/flight-reservation-system/pull/25) | 2026-03-06 |

### Notas del Sprint 2
- US-08, US-09, US-10, US-11 completadas en batch 1 (las 4 en paralelo con Agents worktree)
- US-09 y US-10 requirieron rebase por conflicto en conftest.py (resueltos)
- 45 tests unitarios nuevos: 20 (flights) + 12 (bookings) + 13 (auth/schemas)
- pytest-cov configurado con threshold >80% en CI
- US-12/US-13 combinadas en un solo PR (frontend scaffolding + auth store acoplados)
- US-14, US-15 en paralelo con Agents worktree (batch 2)
- US-14 requirio rebase por conflictos en frontend/ con US-12/13 (resueltos: solo DashboardPage.tsx cambiado)
- US-15 sobreescribio pyproject.toml (corregido con fix commit post-merge)
- Frontend: Vite + React + TS + Tailwind CSS v4 + Zustand + Axios
- Sprint 2 completado: 33/33 SP

---

## Sprint 3 — Frontend Completo

**Sprint Goal:** Completar todas las paginas del frontend con funcionalidad real.
**Duracion:** Semana 5-6
**Estado:** COMPLETADO
**SP Completados:** 34/34

```
Sprint 3: [######################################] 100%  (34/34 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-16 | Lista de destinos y vuelos disponibles | 5 | DONE | `feature/s3-US16-lista-vuelos` | [#27](https://github.com/jdabid/flight-reservation-system/pull/27) | 2026-03-07 |
| US-17 | Crear destinos y vuelos desde frontend | 5 | DONE | `feature/s3-US17-crear-vuelos` | [#28](https://github.com/jdabid/flight-reservation-system/pull/28) | 2026-03-07 |
| US-18 | Crear reserva con precio en tiempo real | 8 | DONE | `feature/s3-US18-crear-reserva` | [#29](https://github.com/jdabid/flight-reservation-system/pull/29) | 2026-03-07 |
| US-19 | Historial de reservas | 3 | DONE | `feature/s3-US19-historial-reservas` | [#30](https://github.com/jdabid/flight-reservation-system/pull/30) | 2026-03-07 |
| US-20 | Graficas de estadisticas | 5 | DONE | `feature/s3-US20-graficas-estadisticas` | [#31](https://github.com/jdabid/flight-reservation-system/pull/31) | 2026-03-07 |
| US-21 | Chat con agente IA | 5 | DONE | `feature/s3-US21-chat-ia` | [#32](https://github.com/jdabid/flight-reservation-system/pull/32) | 2026-03-07 |
| US-22 | Dockerfile para frontend con nginx | 3 | DONE | `feature/s3-US22-dockerfile-frontend` | [#33](https://github.com/jdabid/flight-reservation-system/pull/33) | 2026-03-07 |

### Notas del Sprint 3
- US-16 a US-19 implementadas secuencialmente desde contexto principal (agentes bloqueados por permisos)
- US-20, US-21, US-22 implementadas en paralelo con Agents worktree (permisos wildcard configurados)
- US-21 requirio rebase por conflicto en App.tsx y Layout.tsx con US-20 (resuelto)
- US-22 sin conflictos (solo archivos de infra)
- Nuevas paginas: FlightsPage, CreateFlightPage, BookingPage, BookingsPage, StatsPage, ChatPage
- Recharts agregado para graficas interactivas
- Dockerfile multi-stage + nginx para produccion del frontend
- Sprint 3 completado: 34/34 SP

---

## Sprint 4 — Docker Profesional + Kubernetes Base

**Sprint Goal:** Contenedorizacion profesional y despliegue base en Kubernetes con Helm.
**Duracion:** Semana 7-8
**Estado:** COMPLETADO
**SP Completados:** 32/32

```
Sprint 4: [######################################] 100%  (32/32 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-23 | Docker Compose con todos los servicios | 5 | DONE | `feature/s4-US23-docker-compose-pro` | [#34](https://github.com/jdabid/flight-reservation-system/pull/34) | 2026-03-07 |
| US-24 | Docker Compose dev con hot-reload | 3 | DONE | `feature/s4-US24-docker-dev` | [#35](https://github.com/jdabid/flight-reservation-system/pull/35) | 2026-03-07 |
| US-25 | Makefile con comandos rapidos | 2 | DONE | `feature/s4-US25-makefile` | [#36](https://github.com/jdabid/flight-reservation-system/pull/36) | 2026-03-07 |
| US-26 | Helm Chart con templates | 8 | DONE | `feature/s4-US26-helm-chart` | [#37](https://github.com/jdabid/flight-reservation-system/pull/37) | 2026-03-07 |
| US-27 | HPA para autoescalado | 3 | DONE | `feature/s4-US27-hpa-autoescalado` | [#38](https://github.com/jdabid/flight-reservation-system/pull/38) | 2026-03-07 |
| US-28 | Ingress controller con TLS | 5 | DONE | `feature/s4-US28-ingress-tls` | [#39](https://github.com/jdabid/flight-reservation-system/pull/39) | 2026-03-07 |
| US-29 | Network policies | 3 | DONE | `feature/s4-US29-network-policies` | [#40](https://github.com/jdabid/flight-reservation-system/pull/40) | 2026-03-07 |
| US-30 | Resource requests y limits | 3 | DONE | `feature/s4-US30-resource-limits` | [#41](https://github.com/jdabid/flight-reservation-system/pull/41) | 2026-03-07 |

### Notas del Sprint 4
- Batch 1 (US-23 a US-26): 4 agentes en paralelo con worktree isolation
- Batch 2 (US-27 a US-30): 4 agentes en paralelo con worktree isolation
- US-29 requirio rebase por conflicto en values.yaml con US-28 (resuelto: mantener ambas secciones)
- US-30 rebase limpio sin conflictos
- Helm chart profesional con _helpers.tpl, deployments separados (API/Worker), HPA v2, Ingress TLS, NetworkPolicies
- Makefile con 22 targets para desarrollo rapido
- Sprint 4 completado: 32/32 SP

---

## Sprint 5 — Kustomize + IA Avanzada

**Sprint Goal:** Configurar ambientes con Kustomize y mejorar el agente de IA con RAG avanzado.
**Duracion:** Semana 9-10
**Estado:** COMPLETADO
**SP Completados:** 33/33

```
Sprint 5: [######################################] 100%  (33/33 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-31 | Kustomize base con manifiestos | 5 | DONE | `feature/s5-US31-kustomize-base` | [#42](https://github.com/jdabid/flight-reservation-system/pull/42) | 2026-03-07 |
| US-32 | Overlays para dev, staging, prod | 5 | DONE | `feature/s5-US32-kustomize-overlays` | [#43](https://github.com/jdabid/flight-reservation-system/pull/43) | 2026-03-07 |
| US-33 | Kustomize build valido por ambiente | 3 | DONE | `feature/s5-US33-kustomize-validate` | [#44](https://github.com/jdabid/flight-reservation-system/pull/44) | 2026-03-07 |
| US-34 | pgvector en PostgreSQL | 5 | DONE | `feature/s5-US34-pgvector` | [#45](https://github.com/jdabid/flight-reservation-system/pull/45) | 2026-03-07 |
| US-35 | Busqueda semantica en agente IA | 5 | DONE | `feature/s5-US35-busqueda-semantica` | [#46](https://github.com/jdabid/flight-reservation-system/pull/46) | 2026-03-07 |
| US-36 | Prediccion de demanda por destino | 5 | DONE | `feature/s5-US36-prediccion-demanda` | [#47](https://github.com/jdabid/flight-reservation-system/pull/47) | 2026-03-07 |
| US-37 | Tool calling en agente IA | 5 | DONE | `feature/s5-US37-tool-calling` | [#48](https://github.com/jdabid/flight-reservation-system/pull/48) | 2026-03-07 |

### Notas del Sprint 5
- Batch 1 (US-31 a US-34): 4 agentes en paralelo con worktree isolation
- Batch 2 (US-35 a US-37): 3 agentes en paralelo con worktree isolation
- US-32 y US-33 conflictos en kustomize base (REC-01): ambos crearon archivos base, resuelto tomando master
- US-36 conflicto en tools.py y ai.py con US-35 (REC-01): mantener ambas funciones
- US-37 conflicto en ai.py con US-35/36: refactorizar a tool calling integrando todas las tools
- Worktrees anidados (ERR-S4-03 recurrente): batch 2 dentro de worktree residual de US-33
- Agente IA refactorizado de prompt-stuffing a LangChain tool calling real
- Sprint 5 completado: 33/33 SP

---

## Sprint 6 — Message Queue + Observabilidad

**Sprint Goal:** Robustecer el procesamiento asincrono y agregar observabilidad completa.
**Duracion:** Semana 11-12
**Estado:** COMPLETADO
**SP Completados:** 32/32

```
Sprint 6: [######################################] 100%  (32/32 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-38 | Dead letter queue | 3 | DONE | `feature/s6-US38-dead-letter-queue` | [#49](https://github.com/jdabid/flight-reservation-system/pull/49) | 2026-03-07 |
| US-39 | Flower para monitorear Celery | 3 | DONE | `feature/s6-US39-flower-monitoring` | [#50](https://github.com/jdabid/flight-reservation-system/pull/50) | 2026-03-07 |
| US-40 | Nuevas tasks de notificaciones | 5 | DONE | `feature/s6-US40-notification-tasks` | [#51](https://github.com/jdabid/flight-reservation-system/pull/51) | 2026-03-07 |
| US-41 | Event log de reservas | 3 | DONE | `feature/s6-US41-event-log` | [#52](https://github.com/jdabid/flight-reservation-system/pull/52) | 2026-03-07 |
| US-42 | Metricas de Prometheus | 5 | DONE | `feature/s6-US42-prometheus-metrics` | [#53](https://github.com/jdabid/flight-reservation-system/pull/53) | 2026-03-07 |
| US-43 | Dashboards de Grafana | 5 | DONE | `feature/s6-US43-grafana-dashboards` | [#54](https://github.com/jdabid/flight-reservation-system/pull/54) | 2026-03-07 |
| US-44 | Tracing con OpenTelemetry | 5 | DONE | `feature/s6-US44-opentelemetry-tracing` | [#55](https://github.com/jdabid/flight-reservation-system/pull/55) | 2026-03-07 |
| US-45 | Logging JSON con correlation IDs | 3 | DONE | `feature/s6-US45-json-logging` | [#56](https://github.com/jdabid/flight-reservation-system/pull/56) | 2026-03-07 |

### Notas del Sprint 6
- Batch 1 (US-38 a US-41): 4 agentes en paralelo con worktree isolation
- Batch 2 (US-42 a US-45): 4 agentes en paralelo con worktree isolation
- US-40 conflicto en stats.py con US-38 (REC-01): mantener ambos endpoints
- US-41 conflicto en commands.py con US-40 (REC-01): mantener ambas dispatches
- US-43 conflicto en docker-compose.yml con US-42 (REC-01): mantener prometheus y grafana
- US-44 conflicto en 4 archivos (requirements.txt, main.py, docker-compose.yml, Makefile): agregar OTel + Jaeger
- US-45 conflicto en 3 archivos: agregar logging JSON + correlation IDs
- Worktrees anidados recurrentes (ERR-S4-03): batch 2 dentro de worktree residual de US-41
- Observabilidad completa: Prometheus + Grafana + Jaeger + JSON logging con correlation IDs
- Sprint 6 completado: 32/32 SP

---

## Sprint 7 — Terraform + CI/CD + Deploy Publico

**Sprint Goal:** Infraestructura como codigo, pipeline completo y deploy publico funcional.
**Duracion:** Semana 13-14
**Estado:** NO INICIADO
**SP Completados:** 0/33

```
Sprint 7: [______________________________________] 0%  (0/33 SP)
```

| ID | User Story | SP | Estado | Branch | PR | Fecha |
|----|------------|----|---------|---------|----|-------|
| US-46 | Terraform VPC + EKS | 5 | PENDIENTE | — | — | — |
| US-47 | Terraform RDS + ElastiCache | 5 | PENDIENTE | — | — | — |
| US-48 | Terraform IAM | 3 | PENDIENTE | — | — | — |
| US-49 | Pipeline CI completo | 5 | PENDIENTE | — | — | — |
| US-50 | Pipeline CD staging + prod | 5 | PENDIENTE | — | — | — |
| US-51 | Deploy publico funcional | 5 | PENDIENTE | — | — | — |
| US-52 | Documentacion ADRs, C4, runbook | 3 | PENDIENTE | — | — | — |
| US-53 | README con badges y demo URL | 2 | PENDIENTE | — | — | — |

---

## Burndown Chart

```
Story Points
Restantes
  229 |*
      |
  213 |
      |
  197 |   *
      |
  181 |
      |
  164 |        *
      |
  150 |
      |
  143 |
      |
  130 |              *
      |
   98 |                    *
      |
   65 |                          *
      |
   33 |                                *  ← actual (Sprint 6 completado)
      |
   25 |
      |
    0 |________________________________________________
      S1         S2         S3         S4         S5         S6         S7
```

---

## Historial de Cambios

| Fecha | US | Accion | SP | Herramientas usadas |
|-------|-----|--------|----|---------------------|
| 2026-03-06 | US-01 | COMPLETADA | 3 | Skill: start-user-story, git-workflow, finish-user-story |
| 2026-03-06 | US-02 | COMPLETADA | 5 | Agent (worktree isolation), Skill: git-workflow |
| 2026-03-06 | US-03 | COMPLETADA | 8 | Agent (worktree isolation), Skill: new-feature, git-workflow |
| 2026-03-06 | US-06 | COMPLETADA | 3 | Agent (worktree isolation), Skill: git-workflow |
| 2026-03-06 | US-04 | COMPLETADA | 5 | Agent (worktree isolation), Skill: git-workflow |
| 2026-03-06 | US-05 | COMPLETADA | 3 | Agent (worktree isolation), Skill: git-workflow |
| 2026-03-06 | US-07 | COMPLETADA | 5 | Agent (worktree isolation), Skill: new-feature, git-workflow |
| 2026-03-06 | US-08 | COMPLETADA | 5 | Agent (worktree isolation), pytest |
| 2026-03-06 | US-09 | COMPLETADA | 5 | Agent (worktree isolation), pytest |
| 2026-03-06 | US-10 | COMPLETADA | 3 | Agent (worktree isolation), pytest |
| 2026-03-06 | US-11 | COMPLETADA | 3 | Agent (worktree isolation), pytest-cov |
| 2026-03-06 | US-12 | COMPLETADA | 5 | Agent (worktree isolation), Vite, React, Tailwind |
| 2026-03-06 | US-13 | COMPLETADA | 5 | Agent (worktree isolation), Zustand, Axios |
| 2026-03-06 | US-15 | COMPLETADA | 2 | Agent (worktree isolation), bandit |
| 2026-03-06 | US-14 | COMPLETADA | 5 | Agent (worktree isolation), React, stats API |
| 2026-03-07 | US-16 | COMPLETADA | 5 | Write, Edit, Bash (git), gh CLI |
| 2026-03-07 | US-17 | COMPLETADA | 5 | Write, Edit, Bash (git), gh CLI |
| 2026-03-07 | US-18 | COMPLETADA | 8 | Write, Edit, Bash (git), gh CLI |
| 2026-03-07 | US-19 | COMPLETADA | 3 | Write, Edit, Bash (git), gh CLI |
| 2026-03-07 | US-20 | COMPLETADA | 5 | Agent (worktree isolation), recharts, npm |
| 2026-03-07 | US-21 | COMPLETADA | 5 | Agent (worktree isolation), rebase conflictos |
| 2026-03-07 | US-22 | COMPLETADA | 3 | Agent (worktree isolation), Docker, nginx |
| 2026-03-07 | US-23 | COMPLETADA | 5 | Agent (worktree isolation), Docker Compose |
| 2026-03-07 | US-24 | COMPLETADA | 3 | Agent (worktree isolation), Docker Compose dev |
| 2026-03-07 | US-25 | COMPLETADA | 2 | Agent (worktree isolation), Makefile |
| 2026-03-07 | US-26 | COMPLETADA | 8 | Agent (worktree isolation), Helm, _helpers.tpl |
| 2026-03-07 | US-27 | COMPLETADA | 3 | Agent (worktree isolation), Helm HPA v2 |
| 2026-03-07 | US-28 | COMPLETADA | 5 | Agent (worktree isolation), Helm Ingress TLS |
| 2026-03-07 | US-29 | COMPLETADA | 3 | Agent (worktree isolation), Helm NetworkPolicy |
| 2026-03-07 | US-30 | COMPLETADA | 3 | Agent (worktree isolation), Helm resources |
| 2026-03-07 | US-31 | COMPLETADA | 5 | Agent (worktree isolation), Kustomize |
| 2026-03-07 | US-32 | COMPLETADA | 5 | Agent (worktree isolation), Kustomize overlays |
| 2026-03-07 | US-33 | COMPLETADA | 3 | Agent (worktree isolation), Bash, Makefile |
| 2026-03-07 | US-34 | COMPLETADA | 5 | Agent (worktree isolation), pgvector, SQLAlchemy |
| 2026-03-07 | US-35 | COMPLETADA | 5 | Agent (worktree isolation), LangChain RAG |
| 2026-03-07 | US-36 | COMPLETADA | 5 | Agent (worktree isolation), Redis stats, LangChain |
| 2026-03-07 | US-37 | COMPLETADA | 5 | Agent (worktree isolation), LangChain AgentExecutor |
| 2026-03-07 | US-38 | COMPLETADA | 3 | Agent (worktree isolation), Celery DLQ |
| 2026-03-07 | US-39 | COMPLETADA | 3 | Agent (worktree isolation), Flower |
| 2026-03-07 | US-40 | COMPLETADA | 5 | Agent (worktree isolation), Celery tasks |
| 2026-03-07 | US-41 | COMPLETADA | 3 | Agent (worktree isolation), SQLAlchemy event log |
| 2026-03-07 | US-42 | COMPLETADA | 5 | Agent (worktree isolation), Prometheus |
| 2026-03-07 | US-43 | COMPLETADA | 5 | Agent (worktree isolation), Grafana dashboards |
| 2026-03-07 | US-44 | COMPLETADA | 5 | Agent (worktree isolation), OpenTelemetry, Jaeger |
| 2026-03-07 | US-45 | COMPLETADA | 3 | Agent (worktree isolation), python-json-logger |
