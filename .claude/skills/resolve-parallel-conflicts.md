# Skill: Resolve Parallel Conflicts (REC-01)

Resuelve conflictos de merge cuando multiples agents en worktree paralelo modificaron los mismos archivos.

## Cuando usar

Despues de mergear una branch de agent y la siguiente falla con:
```
Pull request #XX is not mergeable: the merge commit cannot be cleanly created
```
o al hacer `git rebase master`:
```
CONFLICT (add/add): Merge conflict in {archivo}
CONFLICT (content): Merge conflict in {archivo}
```

## Procedimiento

### 1. Identificar tipo de conflicto

```bash
git rebase master 2>&1 | grep "CONFLICT"
```

Clasificar cada archivo conflictivo:

| Tipo | Descripcion | Estrategia |
|------|-------------|------------|
| **Archivo compartido con cambios independientes** | Ambos modificaron zonas distintas del mismo archivo (ej: main.py con nuevos routers) | Combinar ambos cambios |
| **Archivo compartido con cambios solapados** | Ambos modificaron la misma zona (ej: conftest.py con mocks distintos) | HEAD como base + agregar lo nuevo de theirs |
| **Archivo creado por ambos** (add/add) | Ambos crearon el mismo archivo (ej: frontend scaffolding) | Evaluar cual es mas completo |
| **Solo un archivo importa** | Agent duplico scaffolding pero solo aporta 1 archivo unico | `--ours` para todo excepto el archivo unico |

### 2. Resolver segun estrategia

**Para archivos donde HEAD (master) tiene la version correcta:**
```bash
git checkout --ours path/to/file.py
```

**Para archivos donde la branch tiene la version correcta:**
```bash
git checkout --theirs path/to/file.py
```

**Para archivos que necesitan combinacion manual:**
1. Leer el archivo con marcadores de conflicto
2. Identificar que aporta cada lado:
   - HEAD (master): lo que ya esta mergeado de branches anteriores
   - Branch: lo nuevo de esta US
3. Escribir la version combinada con Write
4. Regla de oro: HEAD como base, agregar SOLO lo nuevo de la branch

### 3. Completar el rebase

```bash
git add {archivos-resueltos}
GIT_EDITOR=true git rebase --continue
```

### 4. Force push y merge

```bash
git push -f origin {branch-name}
gh pr merge {PR-number} --merge --delete-branch
```

## Archivos con conflictos frecuentes

| Archivo | Sprints afectados | Motivo |
|---------|-------------------|--------|
| `backend/src/main.py` | S1 (US-03,05,07) | Cada feature agrega imports y routers |
| `backend/tests/unit/conftest.py` | S2 (US-09,10) | Cada test suite agrega mocks y model imports |
| `frontend/src/pages/DashboardPage.tsx` | S2 (US-14) | Scaffolding duplicado por agent |
| `backend/pyproject.toml` | S2 (US-15) | Config compartida de multiples tools |

## Prevencion (antes de lanzar agents paralelos)

1. **Identificar archivos compartidos** que multiples US modificaran
2. **Pre-crear archivos compartidos** en master antes de lanzar agents:
   - conftest.py con todos los mocks necesarios
   - main.py con imports placeholder
3. **Ordenar merges**: mergear primero la US con mas cambios en archivos compartidos
4. **Instrucciones al agent**: "NO modificar {archivo}. Solo crear archivos nuevos."
