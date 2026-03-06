# Skill: Cleanup Worktrees (REC-02)

Limpia worktrees de agents y sus branches locales despues de mergear PRs.

## Cuando usar

Despues de `gh pr merge --delete-branch` cuando aparece:
```
failed to delete local branch feature/xxx: Cannot delete branch 'feature/xxx' checked out at '.claude/worktrees/agent-xxx'
```

O al final de un batch de agents paralelos, para limpiar todos los worktrees.

## Limpiar un worktree especifico

```bash
# 1. Eliminar el worktree (--force porque tiene branch checked out)
git worktree remove .claude/worktrees/agent-{id} --force

# 2. Eliminar la branch local (ya fue eliminada en remote por el merge)
git branch -D feature/sX-USXX-xxx
```

## Limpiar TODOS los worktrees de agents

Usar despues de completar un batch completo de agents:

```bash
# Listar worktrees activos
git worktree list

# Eliminar todos los worktrees de agents
for wt in .claude/worktrees/agent-*; do
  [ -d "$wt" ] && git worktree remove "$wt" --force 2>/dev/null
done

# Limpiar branches locales huerfanas (ya mergeadas)
git fetch --prune origin
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs -r git branch -D
```

## Limpiar antes de lanzar nuevos agents

Ejecutar SIEMPRE antes de un nuevo batch para evitar conflictos:

```bash
# Verificar que no hay worktrees colgados
git worktree list | grep -c "worktrees/agent" || echo "Limpio"

# Prune worktrees con directorios ya eliminados
git worktree prune
```

## Orden de operaciones post-merge

1. `gh pr merge {N} --merge --delete-branch` (ignora error de branch local)
2. `git worktree remove .claude/worktrees/agent-{id} --force`
3. `git branch -D {branch-name}` (si aun existe)
4. `git checkout master && git pull origin master`
5. Continuar con el siguiente merge o batch
