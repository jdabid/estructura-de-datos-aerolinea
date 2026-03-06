# Errores Sprint 1 — Fundamentos Backend

> Sprint 1: US-01 a US-07 | 32 SP | Completado 2026-03-06

---

## ERR-S1-01: Conflicto en main.py al mergear US-03 tras US-02

**Severidad:** Alta
**US afectada:** US-03 (JWT Auth)
**Recurrente:** Si → REC-01

### Descripcion
US-02 elimino `create_all()` y los imports de `engine`/`Base` de `main.py`. US-03, desarrollada en paralelo, agrego imports de `engine`/`Base` y el router de auth. Al hacer rebase de US-03 sobre master (ya con US-02 mergeado), el conflicto dejaba imports contradictorios.

### Causa raiz
Ambas US modificaron `main.py` en paralelo (worktree isolation). US-02 quito lineas que US-03 agregaba imports alrededor de ellas.

### Solucion aplicada
Rebase manual: se combinaron correctamente los imports (sin `create_all`, con auth router), se mantuvo el comentario de Alembic de US-02.

### Prevencion
Skill `resolve-parallel-conflicts.md` creado para estandarizar la resolucion.

---

## ERR-S1-02: Conflicto en main.py al mergear US-05 (CORS/Middleware)

**Severidad:** Alta
**US afectada:** US-05 (CORS + Rate Limiting)
**Recurrente:** Si → REC-01

### Descripcion
US-04 agrego el `app_exception_handler` en `main.py`. US-05 agrego `CORSMiddleware` y `RateLimitMiddleware`. Al hacer rebase, ambos bloques colisionaron en la zona de configuracion del app.

### Causa raiz
Mismo patron que ERR-S1-01: multiples agents modificando `main.py` en paralelo.

### Solucion aplicada
Rebase manual: se mantuvieron AMBOS — exception handler de US-04 Y middlewares de US-05.

---

## ERR-S1-03: Conflicto en main.py al mergear US-07 (Stats)

**Severidad:** Media
**US afectada:** US-07 (Stats Feature)
**Recurrente:** Si → REC-01

### Descripcion
US-07 solo necesitaba agregar `from src.api.v1 import stats` y `app.include_router(stats.router)`, pero su branch partia de un main.py sin los cambios de US-04/05/06.

### Causa raiz
Mismo patron REC-01.

### Solucion aplicada
Rebase: se mantuvo todo el codigo existente de master y se agrego solo el import y router de stats.

---

## ERR-S1-04: Worktree branch no se puede eliminar post-merge

**Severidad:** Baja
**US afectada:** Varias (US-02, US-03, US-06)
**Recurrente:** Si → REC-02

### Descripcion
Despues de `gh pr merge --delete-branch`, el comando elimina la branch remota pero falla al eliminar la local porque sigue checked out en el worktree del agent.

### Error exacto
```
error: Cannot delete branch 'feature/s1-US02-alembic-migraciones' checked out at '.claude/worktrees/agent-xxx'
```

### Causa raiz
`gh pr merge --delete-branch` intenta `git branch -d` sobre una branch que aun tiene un worktree asociado. Git no permite eliminar branches checked out.

### Solucion aplicada
```bash
git worktree remove .claude/worktrees/agent-xxx --force
git branch -D feature/s1-USxx-xxx
```

### Prevencion
Skill `cleanup-worktrees.md` creado para automatizar la limpieza.

---

## ERR-S1-05: Cambios sin stage bloquean rebase

**Severidad:** Baja
**US afectada:** US-05

### Descripcion
Al intentar rebase de US-05 sobre master actualizado, git rechazo porque `.claude/skills/finish-user-story.md` tenia cambios locales sin commitear.

### Causa raiz
El archivo fue editado durante la sesion (actualizacion del skill) pero no se hizo commit antes del rebase.

### Solucion aplicada
```bash
git stash
git rebase master
git stash pop
```

---

## ERR-S1-06: PR no mergeable tras force push

**Severidad:** Baja
**US afectada:** US-05

### Descripcion
Despues de hacer `git push -f` con la branch rebaseada, GitHub no reconocia inmediatamente la branch como libre de conflictos.

### Causa raiz
GitHub necesita unos segundos para recalcular el estado de mergeabilidad despues de un force push.

### Solucion aplicada
Esperar unos segundos y reintentar. En casos extremos se uso `--admin` flag.

---

## ERR-S1-07: Error "File modified since read" al resolver conflicto

**Severidad:** Baja
**US afectada:** US-03

### Descripcion
Al resolver el conflicto de main.py, se intento usar Write sin haber re-leido el archivo despues del rebase parcial.

### Causa raiz
Claude Code valida que el archivo no haya cambiado entre Read y Write. El rebase modifico el archivo (insertando marcadores de conflicto), invalidando el Read previo.

### Solucion aplicada
Read del archivo de nuevo (con marcadores de conflicto visibles), luego Write con la version resuelta.

---

## Resumen Sprint 1

| Categoria | Cantidad | Recurrentes |
|-----------|----------|-------------|
| Conflictos merge paralelo | 3 | Si (REC-01) |
| Worktree cleanup | 1 | Si (REC-02) |
| Git state issues | 2 | No |
| Tool usage | 1 | No |
| **Total** | **7** | **4** |
