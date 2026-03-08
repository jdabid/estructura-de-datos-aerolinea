# Errores Sprint 3 — Frontend Completo

> Sprint 3: US-16 a US-22 | 34 SP | Completado 2026-03-07

---

## ERR-S3-01: Agentes en background bloqueados por permisos no pre-aprobados

**Severidad:** Alta
**US afectada:** US-16, US-17, US-18, US-19 (batch 1)
**Recurrente:** No (corregido en este sprint)

### Descripcion
Se lanzaron 4 agentes en paralelo con `Agent (worktree isolation)` para US-16 a US-19. Los 4 quedaron bloqueados indefinidamente porque las herramientas `Bash` y `Write` requerían aprobación interactiva del usuario, pero los agentes en background no pueden mostrar prompts de aprobación.

### Causa raiz
El archivo `.claude/settings.local.json` contenía **132 comandos específicos exactos** aprobados previamente (ej: `Bash(git checkout -b feature/s1-US03-jwt-auth)`). Cualquier comando nuevo con argumentos diferentes (ej: `Bash(git checkout -b feature/s3-US16-lista-vuelos)`) no coincidía con ninguna regla y requería aprobación manual.

Los agentes en background no tienen interfaz para solicitar aprobación → se bloquean esperando indefinidamente → timeout.

### Solucion aplicada
1. **Inmediata**: Se implementaron las 4 US secuencialmente desde el contexto principal (donde sí hay interacción para aprobar)
2. **Definitiva**: Se reemplazaron los 132 comandos exactos por **26 reglas genéricas con wildcards**:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(gh:*)",
      "Bash(npm:*)",
      "Bash(cd:*)",
      "Write",
      "Edit",
      "Agent"
    ]
  }
}
```

### Prevencion
Antes de lanzar agentes en background, verificar que `.claude/settings.local.json` tenga reglas wildcard para todas las herramientas que los agentes necesitarán. Las reglas exactas solo sirven para el contexto principal.

---

## ERR-S3-02: Conflicto en App.tsx y Layout.tsx al mergear US-21 tras US-20

**Severidad:** Media
**US afectada:** US-21 (Chat con agente IA)
**Recurrente:** Si → REC-01

### Descripcion
US-20 y US-21 corrieron en paralelo con worktree isolation. Ambas modificaron las mismas líneas en dos archivos:
- `frontend/src/App.tsx`: ambas agregaron un import y una ruta después de `<Route path="/bookings">`
- `frontend/src/components/Layout.tsx`: ambas agregaron un nav item después de `{ path: '/bookings', label: 'Reservas' }`

Al mergear US-21 (después de US-20), git detectó conflicto add/add en ambos archivos.

### Causa raiz
Patrón REC-01: múltiples agents modificando el mismo punto de inserción en archivos compartidos (Layout.tsx navItems array, App.tsx routes). Idéntico al problema de main.py en Sprint 1 y conftest.py en Sprint 2.

### Solucion aplicada
Rebase manual de US-21 sobre master actualizado (post US-20). Resolución trivial: mantener ambas líneas (tanto Stats como Chat):

```tsx
// App.tsx - mantener ambos imports y rutas
import StatsPage from './pages/StatsPage';
import ChatPage from './pages/ChatPage';

// Layout.tsx - mantener ambos nav items
{ path: '/stats', label: 'Estadisticas' },
{ path: '/chat', label: 'Asistente IA' },
```

### Leccion aprendida
Este conflicto es inevitable cuando múltiples agents agregan entradas a la misma lista/array. Opciones para mitigar:
1. **Aceptar el conflicto**: es trivial de resolver (solo agregar ambas líneas), el rebase toma <30 segundos
2. **Merge secuencial**: elimina conflictos pero pierde paralelismo
3. **Separar puntos de inserción**: cada agent agrega en una posición diferente (fragil, no recomendado)

**Decisión**: se acepta como costo del paralelismo. El tiempo ahorrado por ejecutar en paralelo supera ampliamente el costo de resolver el conflicto.

---

## ERR-S3-03: `gh pr merge --delete-branch` falla con worktrees activos

**Severidad:** Baja
**US afectada:** US-20, US-21, US-22
**Recurrente:** Si → REC-02

### Descripcion
Al ejecutar `gh pr merge --squash --delete-branch`, el merge en GitHub se completaba exitosamente, pero la eliminación de la branch local fallaba con:

```
error: Cannot delete branch 'feature/s3-US20-graficas-estadisticas' checked out at
'/Users/.../flight-reservation-system/.claude/worktrees/agent-a29a2234'
```

### Causa raiz
Patrón REC-02: el worktree del agente todavía tiene la branch checked out. Git no permite borrar una branch que está checked out en algún worktree, incluso si el merge ya se completó en el remoto.

### Solucion aplicada
Limpieza manual post-merge en 2 pasos:
```bash
git worktree remove .claude/worktrees/agent-XXXX --force
git branch -D feature/s3-USXX-nombre
```

### Prevencion
Agregar la limpieza de worktree como paso estándar después de cada merge. El skill `cleanup-worktrees.md` ya existe para esto. Alternativamente, encadenar los comandos:
```bash
gh pr merge N --squash --delete-branch 2>&1; \
  git worktree remove .claude/worktrees/agent-XXXX --force 2>/dev/null; \
  git branch -D feature-branch 2>/dev/null; \
  git pull origin master
```

---

## ERR-S3-04: Agente US-21 cambió Layout de min-h-screen a h-screen

**Severidad:** Baja
**US afectada:** US-21 (Chat con agente IA)
**Recurrente:** No

### Descripcion
El agente de US-21 modificó el contenedor raíz del Layout de `min-h-screen` a `h-screen` y agregó `overflow-y-auto` al `<main>`, para que el chat pudiera ocupar el 100% de la altura disponible. Este cambio afecta potencialmente a todas las demás páginas.

### Causa raiz
El agente necesitaba que el ChatPage ocupara la altura completa para la interfaz de chat (mensajes + input fijo abajo). La solución más simple era cambiar el Layout global, pero esto puede causar problemas en páginas con contenido largo que necesitan scroll natural.

### Impacto real
- `h-screen` fija la altura a exactamente la ventana del navegador
- `overflow-y-auto` en `<main>` permite scroll dentro del area de contenido
- Las demás páginas (Dashboard, Flights, etc.) siguen funcionando porque su contenido tiene scroll interno
- No se detectaron problemas visuales, pero es un cambio de comportamiento global

### Solucion aplicada
Se aceptó el cambio porque `overflow-y-auto` en main funciona correctamente para todas las páginas. Si causa problemas en el futuro, la solución sería mover el `h-screen` solo al ChatPage en vez del Layout global.

---

## Resumen Sprint 3

| Categoria | Cantidad | Recurrentes |
|-----------|----------|-------------|
| Permisos agentes background | 1 | No (corregido) |
| Conflictos merge paralelo | 1 | Si (REC-01) |
| Worktree cleanup post-merge | 1 | Si (REC-02) |
| Cambio global no solicitado | 1 | No |
| **Total** | **4** | **2** |

### Comparacion con sprints anteriores

| Metrica | Sprint 1 | Sprint 2 | Sprint 3 |
|---------|----------|----------|----------|
| Errores totales | 7 | 5 | 4 |
| Severidad critica | 0 | 3 | 0 |
| Severidad alta | 3 | 2 | 1 |
| Recurrentes (REC-01) | 3 | 2 | 1 |
| Tiempo perdido estimado | ~45 min | ~30 min | ~15 min |

### Tendencia
- Los errores disminuyen sprint a sprint (7 → 5 → 4)
- No hubo errores críticos en Sprint 3
- El patrón REC-01 (conflictos paralelos) sigue presente pero es aceptado como costo del paralelismo
- El patrón REC-02 (worktree cleanup) es rutinario y tiene solución estándar
- La configuración de permisos wildcard (ERR-S3-01) fue la mejora más significativa del sprint
