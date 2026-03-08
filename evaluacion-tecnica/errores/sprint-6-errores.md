# Errores Sprint 6 — Message Queue + Observabilidad

> Sprint 6: US-38 a US-45 | 32 SP | Completado 2026-03-07

---

## ERR-S6-01: Conflicto en stats.py al mergear US-40 tras US-38

**Severidad:** Baja
**US afectada:** US-40 (Notification Tasks)
**Recurrente:** Si → REC-01

### Descripcion
US-38 (DLQ) y US-40 (Notifications) agregaron endpoints al mismo archivo `src/api/v1/stats.py`:
- US-38 agregó `GET /stats/dead-letters`
- US-40 agregó `GET /stats/notifications`

Al mergear US-40, git detectó conflicto add/add en la zona de endpoints del router.

### Causa raiz
Patrón REC-01: múltiples agents modificando el mismo punto de inserción en archivos compartidos. Archivo convergente del Sprint 6: `stats.py`.

### Solucion aplicada
Rebase manual, mantener ambos endpoints en el router.

### Tiempo perdido
~2 minutos (resolución mecánica).

---

## ERR-S6-02: Conflicto en commands.py al mergear US-41 tras US-40

**Severidad:** Baja
**US afectada:** US-41 (Event Log)
**Recurrente:** Si → REC-01

### Descripcion
US-40 y US-41 modificaron `src/features/bookings/commands.py`:
- US-40 agregó `send_booking_confirmation.delay()` dispatch
- US-41 agregó `log_booking_event()` call

Ambas modificaciones en la misma función `create_booking()`.

### Causa raiz
Patrón REC-01: ambos agents insertaron código en el mismo punto de la función `create_booking()`.

### Solucion aplicada
Mantener ambos: dispatch de notificación + log de evento en `create_booking()`. Merge de imports.

### Tiempo perdido
~2 minutos.

---

## ERR-S6-03: Conflicto en docker-compose.yml al mergear US-43 tras US-42

**Severidad:** Media
**US afectada:** US-43 (Grafana)
**Recurrente:** Si → REC-01

### Descripcion
US-42 (Prometheus) y US-43 (Grafana) agregaron servicios al `docker-compose.yml`:
- US-42 agregó servicio `prometheus` con volumenes y healthcheck
- US-43 agregó servicio `grafana` con provisioning y dashboards

Conflictos en: sección services (add/add), sección volumes (add/add).

### Causa raiz
Patrón REC-01: docker-compose.yml como archivo convergente (similar a values.yaml en Sprint 4).

### Solucion aplicada
Mantener ambos servicios, agregar `depends_on: prometheus` a grafana, mantener ambos named volumes.

### Tiempo perdido
~3 minutos.

---

## ERR-S6-04: Conflicto cuádruple en US-44 (OpenTelemetry)

**Severidad:** Alta
**US afectada:** US-44 (OpenTelemetry Tracing)
**Recurrente:** Si → REC-01

### Descripcion
US-44 entró en conflicto con 4 archivos al rebasar sobre master (que ya tenía US-42 Prometheus y US-43 Grafana mergeados):
1. `backend/requirements.txt` — US-44 agregó OTel deps, master tenía prometheus deps
2. `backend/src/main.py` — US-44 agregó tracing imports, master tenía metrics imports
3. `docker-compose.yml` — US-44 agregó OTEL env vars, master tenía prometheus/grafana services
4. `Makefile` — US-44 agregó jaeger target, master tenía grafana target

### Causa raiz
Patrón REC-01 amplificado: US-44 tocó 4 archivos compartidos simultáneamente. Cada uno con cambios de otros PRs del batch.

### Solucion aplicada
Resolución archivo por archivo:
- `requirements.txt`: mantener prometheus + OTel deps bajo `# Observability`
- `main.py`: mantener ambos imports (metrics + tracing) y ambos setups
- `docker-compose.yml`: checkout master version, agregar OTEL env vars a api/worker, agregar servicio jaeger
- `Makefile`: checkout master version, agregar target jaeger

### Tiempo perdido
~8 minutos (el conflicto más complejo del sprint por tocar 4 archivos).

---

## ERR-S6-05: Worktrees anidados (recurrencia ERR-S4-03)

**Severidad:** Baja
**US afectada:** US-42, US-43, US-44, US-45
**Recurrente:** Si → ERR-S4-03

### Descripcion
El batch 2 (US-42 a US-45) se lanzó con agentes que crearon worktrees dentro del worktree residual de US-41 (agent-abc0d7aa), resultando en paths como:
```
.claude/worktrees/agent-abc0d7aa/.claude/worktrees/agent-af2a15c8
```

### Causa raiz
Mismo patrón de Sprint 4 y Sprint 5: el worktree del batch 1 no se eliminó completamente antes de lanzar batch 2, y los agentes del batch 2 heredaron ese directorio como working directory.

### Solucion aplicada
Worktrees funcionales a pesar de estar anidados. Limpieza manual post-merge con `git worktree remove --force`.

### Tiempo perdido
~1 minuto (operación conocida, resolución inmediata).

---

## Resumen

| Error | Severidad | Patron | Tiempo perdido |
|-------|-----------|--------|----------------|
| ERR-S6-01 | Baja | REC-01 | ~2 min |
| ERR-S6-02 | Baja | REC-01 | ~2 min |
| ERR-S6-03 | Media | REC-01 | ~3 min |
| ERR-S6-04 | Alta | REC-01 | ~8 min |
| ERR-S6-05 | Baja | ERR-S4-03 | ~1 min |
| **Total** | — | — | **~16 min** |

### Lecciones aprendidas
1. **REC-01 escala con observabilidad**: Sprint 6 tuvo más conflictos porque los servicios de observabilidad (Prometheus, Grafana, Jaeger, logging) tocan los mismos archivos compartidos (docker-compose.yml, requirements.txt, main.py, Makefile)
2. **Conflictos multi-archivo**: US-44 demostró que un solo PR puede generar conflictos en 4+ archivos cuando toca infraestructura transversal
3. **Resolución mecánica**: todos los conflictos siguen el patrón "mantener ambos lados" — la resolución es predecible y rápida
4. **Worktrees anidados**: patrón conocido desde Sprint 4, impacto mínimo pero sigue ocurriendo
