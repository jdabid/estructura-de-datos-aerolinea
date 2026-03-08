# Errores Sprint 4 — Docker Profesional + Kubernetes Base

> Sprint 4: US-23 a US-30 | 32 SP | Completado 2026-03-07

---

## ERR-S4-01: Conflicto en values.yaml al mergear US-29 tras US-28

**Severidad:** Media
**US afectada:** US-29 (Network Policies)
**Recurrente:** Si → REC-01

### Descripcion
US-28 (Ingress TLS) y US-29 (NetworkPolicies) corrieron en paralelo con worktree isolation. Ambas agregaron secciones nuevas al final de `infra/helm/flight-app/values.yaml`:
- US-28 agregó la sección `ingress:` con hosts, TLS y annotations
- US-29 agregó la sección `networkPolicy:` con `enabled: false`

Al mergear US-29 (después de US-28), git detectó conflicto add/add en la zona final del archivo.

### Causa raiz
Patrón REC-01: múltiples agents modificando el mismo punto de inserción en archivos compartidos. En este caso `values.yaml` — idéntico al patrón visto con `main.py` (Sprint 1), `conftest.py` (Sprint 2), y `App.tsx`/`Layout.tsx` (Sprint 3). Cada sprint tiene su archivo "punto de convergencia".

### Solucion aplicada
Rebase manual de US-29 sobre master actualizado (post US-28). Resolución trivial: mantener ambas secciones:

```yaml
# values.yaml - mantener ambas secciones al final
ingress:
  enabled: false
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: flights.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: flights-tls
      hosts:
        - flights.example.com

networkPolicy:
  enabled: false
```

### Leccion aprendida
El patrón REC-01 se mantiene predecible: cada vez que dos agents agregan contenido al final del mismo archivo, habrá conflicto. El costo de resolución sigue siendo mínimo (~30 segundos).

---

## ERR-S4-02: `gh pr merge --delete-branch` falla con worktrees activos

**Severidad:** Baja
**US afectada:** US-29, US-30
**Recurrente:** Si → REC-02

### Descripcion
Al ejecutar `gh pr merge --squash --delete-branch`, el merge en GitHub se completaba exitosamente, pero la eliminación de la branch local fallaba con:

```
error: Cannot delete branch 'feature/s4-US29-network-policies' checked out at
'/Users/.../flight-reservation-system/.claude/worktrees/agent-ab5372c1/.claude/worktrees/agent-a160c367'
```

Mismo error para US-30 con su worktree correspondiente.

### Causa raiz
Patrón REC-02: el worktree del agente todavía tiene la branch checked out. Git no permite borrar una branch que está checked out en algún worktree. Idéntico a Sprint 3.

### Solucion aplicada
Limpieza post-merge ya estandarizada:
```bash
git worktree remove .claude/worktrees/agent-XXXX --force
git branch -D feature/s4-USXX-nombre
git pull origin master
```

### Nota
Este error es completamente rutinario y la solución es mecánica. Se considera "costo operativo" del uso de worktrees, no un error real. El merge siempre se completa exitosamente en GitHub; solo falla la limpieza local.

---

## ERR-S4-03: Worktrees de Batch 2 creados dentro de worktree residual de Batch 1

**Severidad:** Baja
**US afectada:** US-27, US-28, US-29, US-30 (batch 2)
**Recurrente:** No

### Descripcion
Al lanzar los 4 agentes de Batch 2 (US-27 a US-30), los worktrees se crearon dentro de la ruta de un worktree residual de Batch 1 (US-26):

```
# Ruta esperada:
.claude/worktrees/agent-a160c367/

# Ruta real (anidada):
.claude/worktrees/agent-ab5372c1/.claude/worktrees/agent-a160c367/
```

El worktree `agent-ab5372c1` pertenecía al agente de US-26 de Batch 1 que no fue limpiado antes de lanzar Batch 2.

### Causa raiz
El agente de US-26 dejó su worktree activo después de completar. Cuando se lanzaron los agentes de Batch 2, Claude Code creó los nuevos worktrees desde el contexto del worktree existente en vez del repositorio principal, generando rutas anidadas.

### Impacto real
- **Ninguno funcional**: los agentes trabajaron correctamente con rutas anidadas
- **Rutas más largas**: las rutas absolutas eran más extensas, pero no causaron problemas
- **Limpieza**: requirió limpiar el worktree padre después de los hijos

### Solucion aplicada
Limpieza secuencial: primero worktrees hijos, luego worktree padre:
```bash
git worktree remove .claude/worktrees/agent-ab5372c1/.claude/worktrees/agent-a160c367 --force
git worktree remove .claude/worktrees/agent-ab5372c1/.claude/worktrees/agent-aec6bc44 --force
git worktree remove .claude/worktrees/agent-ab5372c1 --force
```

### Prevencion
Limpiar todos los worktrees de un batch **antes** de lanzar el siguiente batch:
```bash
# Entre batches
git worktree list | grep "\.claude/worktrees" | awk '{print $1}' | xargs -I{} git worktree remove {} --force
```

---

## ERR-S4-04: US-30 basó su rebase sobre master desactualizado

**Severidad:** Baja
**US afectada:** US-30 (Resource limits)
**Recurrente:** No

### Descripcion
El agente de US-30 completó su trabajo basándose en el master previo a US-27/28/29. Al hacer rebase al final del sprint, US-30 necesitaba incorporar los cambios de 4 PRs anteriores (#37, #38, #39, #40) en `values.yaml`.

### Causa raiz
En el flujo de trabajo paralelo, cada agente de Batch 2 partió del mismo punto de master (post-Batch 1). Al mergear secuencialmente US-27 → US-28 → US-29, cada merge actualizaba `values.yaml`. US-30 fue el último en hacer rebase y tenía la mayor divergencia.

### Impacto real
- El rebase de US-30 se completó **sin conflictos** porque sus cambios (reestructurar `resources` en api/worker) tocaban líneas diferentes a las agregadas por US-27 (autoscaling behavior), US-28 (ingress) y US-29 (networkPolicy)
- No hubo pérdida de tiempo

### Leccion aprendida
Cuando los cambios paralelos tocan **secciones diferentes** del mismo archivo, git puede resolver el rebase automáticamente. El patrón REC-01 solo aplica cuando los cambios son en el **mismo punto de inserción**. La separación semántica de `values.yaml` en secciones claras (autoscaling, ingress, networkPolicy, resources) ayudó a evitar conflictos.

---

## Resumen Sprint 4

| Categoria | Cantidad | Recurrentes |
|-----------|----------|-------------|
| Conflictos merge paralelo | 1 | Si (REC-01) |
| Worktree cleanup post-merge | 1 | Si (REC-02) |
| Worktrees anidados | 1 | No |
| Rebase con divergencia | 1 | No |
| **Total** | **4** | **2** |

### Comparacion con sprints anteriores

| Metrica | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|---------|----------|----------|----------|----------|
| Errores totales | 7 | 5 | 4 | 4 |
| Severidad critica | 0 | 3 | 0 | 0 |
| Severidad alta | 3 | 2 | 1 | 0 |
| Severidad media | 2 | 0 | 1 | 1 |
| Severidad baja | 2 | 0 | 2 | 3 |
| Recurrentes (REC-01) | 3 | 2 | 1 | 1 |
| Recurrentes (REC-02) | 0 | 0 | 1 | 1 |
| Tiempo perdido estimado | ~45 min | ~30 min | ~15 min | ~10 min |

### Tendencia
- Errores se estabilizan en 4, pero la **severidad baja drásticamente** (0 criticos, 0 altos)
- Sprint 4 es el primer sprint sin errores de severidad alta o critica
- REC-01 (conflictos paralelos) sigue presente pero controlado y aceptado
- REC-02 (worktree cleanup) es completamente mecánico y rutinario
- El tiempo perdido sigue bajando: 45 → 30 → 15 → 10 minutos
- La infraestructura (Helm values.yaml) presenta el mismo patrón que el código (main.py, App.tsx): archivos compartidos generan conflictos triviales al trabajar en paralelo
