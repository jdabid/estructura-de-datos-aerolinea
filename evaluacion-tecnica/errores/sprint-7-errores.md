# Errores Sprint 7 — Terraform + CI/CD + Deploy Publico

> Sprint 7: US-46 a US-53 | 33 SP | Completado 2026-03-08

---

## ERR-S7-01: Agente US-51 sin acceso a Bash

**Severidad:** Media
**US afectada:** US-51 (Deploy publico funcional)
**Recurrente:** No (primera vez)

### Descripcion
El agente de US-51 creó todos los archivos (docker-compose.prod.yml, deploy.sh, healthcheck.sh, Makefile edits) pero no pudo hacer `chmod +x` ni `git commit` porque Bash fue denegado repetidamente.

### Causa raiz
Permisos de herramientas del agente. El agente intentó usar Bash pero el sistema lo bloqueó. Posiblemente por la configuración de permisos del worktree o timing de aprobación.

### Solucion aplicada
Re-lanzar el agente con instrucciones explícitas de usar Bash. El segundo intento también falló en Bash. Se completó manualmente desde el contexto principal: `chmod +x`, `git add`, `git commit`.

### Tiempo perdido
~3 minutos (relanzamiento + commit manual).

---

## ERR-S7-02: Worktrees anidados (recurrencia ERR-S4-03)

**Severidad:** Baja
**US afectada:** US-50, US-51, US-52, US-53
**Recurrente:** Si → ERR-S4-03

### Descripcion
El batch 2 (US-50 a US-53) creó worktrees dentro del worktree residual de US-46 (agent-afef1aab):
```
.claude/worktrees/agent-afef1aab/.claude/worktrees/agent-a75b97bd  (US-50)
.claude/worktrees/agent-afef1aab/.claude/worktrees/agent-afbfbd84  (US-51)
.claude/worktrees/agent-afef1aab/.claude/worktrees/agent-a9ea7bb5  (US-52)
.claude/worktrees/agent-afef1aab/.claude/worktrees/agent-a1ab8a32  (US-53)
```

### Causa raiz
Patrón conocido desde Sprint 4: worktree del batch 1 no eliminado antes de lanzar batch 2.

### Solucion aplicada
Worktrees funcionales a pesar del anidamiento. Limpieza post-merge con `git worktree remove --force`.

### Tiempo perdido
~1 minuto.

---

## Resumen

| Error | Severidad | Patron | Tiempo perdido |
|-------|-----------|--------|----------------|
| ERR-S7-01 | Media | Nuevo (Bash denegado) | ~3 min |
| ERR-S7-02 | Baja | ERR-S4-03 | ~1 min |
| **Total** | — | — | **~4 min** |

### Lecciones aprendidas
1. **Sprint más limpio**: 0 conflictos REC-01 porque Terraform, CI/CD, docs y README son archivos completamente independientes
2. **Archivos independientes = 0 conflictos**: cuando cada US toca directorios diferentes, el merge secuencial es trivial
3. **Agentes sin Bash**: algunos agentes pueden perder acceso a Bash — tener plan B de commit manual
4. **Worktrees anidados**: patrón persistente pero de bajo impacto, aceptado como trade-off del desarrollo paralelo
