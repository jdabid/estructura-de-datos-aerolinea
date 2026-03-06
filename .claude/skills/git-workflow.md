# Skill: Git Workflow — Branch, Commit & PR Standards

Gestiona el flujo de trabajo Git para cada User Story con convenciones profesionales.

## Convenciones de Branches

### Formato
```
{tipo}/{sprint}-{US-ID}-{descripcion-corta}
```

### Tipos de branch
| Tipo | Uso |
|------|-----|
| `feature/` | Nueva funcionalidad |
| `fix/` | Correccion de bugs |
| `refactor/` | Reestructuracion sin cambio funcional |
| `test/` | Agregar o mejorar tests |
| `docs/` | Documentacion |
| `infra/` | Docker, K8s, Helm, CI/CD, Terraform |
| `chore/` | Tareas de mantenimiento (linting, deps) |

### Ejemplos
```
feature/s1-US01-reorganizar-carpetas
feature/s1-US03-jwt-auth
fix/s2-US10-login-validation
infra/s4-US26-helm-chart
test/s2-US08-flights-unit-tests
docs/s7-US52-architecture-docs
```

## Convenciones de Commits

### Formato (Conventional Commits)
```
{tipo}({scope}): {descripcion}

{cuerpo opcional}

{footer opcional}
```

### Tipos de commit
| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Correccion de bug |
| `refactor` | Cambio interno sin cambio funcional |
| `test` | Agregar o modificar tests |
| `docs` | Documentacion |
| `style` | Formato, linting (sin cambio de logica) |
| `chore` | Tareas de mantenimiento |
| `ci` | Cambios en CI/CD pipeline |
| `perf` | Mejora de rendimiento |
| `infra` | Docker, K8s, Helm, Terraform |

### Scopes validos
```
flights, bookings, auth, ai, stats, worker, shared, api,
docker, helm, k8s, kustomize, terraform, ci, frontend, tests
```

### Reglas de commits
- Descripcion en minusculas, sin punto final
- Maximo 72 caracteres en la primera linea
- Imperativo: "agregar", no "agregado" ni "agrega"
- En espanol (consistente con el proyecto)
- Un commit por cambio logico (no mezclar features)

### Ejemplos
```
feat(auth): agregar endpoint de registro con JWT
feat(bookings): implementar calculo de precio con descuento
fix(bookings): corregir validacion de mascotas en destinos
refactor(shared): centralizar manejo de excepciones
test(flights): agregar tests unitarios para commands
docs(readme): actualizar seccion de arquitectura
ci(pipeline): agregar step de linting con ruff
infra(helm): configurar HPA con target CPU 70%
infra(docker): optimizar multi-stage build
chore(deps): actualizar fastapi a 0.115
```

## Convenciones de Pull Requests

### Titulo del PR
```
[US-{ID}] {tipo}: {descripcion}
```

### Ejemplos de titulo
```
[US-01] feat: reorganizar estructura de carpetas backend
[US-03] feat: agregar autenticacion JWT
[US-08] test: agregar tests unitarios para flights
[US-26] infra: crear Helm Chart con templates
```

### Cuerpo del PR (template)
```markdown
## User Story
**{US-ID}**: {descripcion de la user story}
**Sprint**: {numero}
**Story Points**: {SP}

## Resumen
- {bullet 1: que se hizo}
- {bullet 2: que se hizo}
- {bullet 3: que se hizo}

## Tipo de cambio
- [ ] Nueva funcionalidad (feature)
- [ ] Correccion de bug (fix)
- [ ] Refactorizacion (refactor)
- [ ] Tests
- [ ] Documentacion
- [ ] Infraestructura (Docker, K8s, CI/CD)

## Archivos clave modificados
- `path/to/file1.py` — descripcion del cambio
- `path/to/file2.py` — descripcion del cambio

## Como probar
1. {paso 1}
2. {paso 2}
3. {paso 3}

## Checklist
- [ ] Codigo funcional sin errores
- [ ] Ruff y mypy pasan sin warnings
- [ ] Tests escritos y pasando
- [ ] Documentacion actualizada si aplica
- [ ] Sin credenciales hardcodeadas
- [ ] Sin archivos innecesarios (.DS_Store, __pycache__)
```

## Instrucciones para Claude Code

### Al INICIAR una User Story

1. Verificar que estamos en la rama principal y actualizada:
```bash
git checkout master
git pull origin master
```

2. Crear la nueva branch desde master:
```bash
git checkout -b {tipo}/{sprint}-{US-ID}-{descripcion}
```

3. Confirmar la branch creada:
```bash
git branch --show-current
```

### Durante el DESARROLLO

4. Hacer commits atomicos siguiendo Conventional Commits:
```bash
git add {archivos-especificos}
git commit -m "$(cat <<'EOF'
{tipo}({scope}): {descripcion}

{cuerpo si es necesario}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

5. Reglas de staging:
- NUNCA usar `git add .` o `git add -A`
- Agregar archivos especificos por nombre
- Verificar con `git status` antes de cada commit
- No commitear: `.env`, `__pycache__/`, `.DS_Store`, credenciales

### Al FINALIZAR una User Story

6. Push de la branch:
```bash
git push -u origin {nombre-branch}
```

7. Crear el Pull Request:
```bash
gh pr create --title "[US-{ID}] {tipo}: {descripcion}" --body "$(cat <<'EOF'
## User Story
**US-{ID}**: {descripcion}
**Sprint**: {N}
**Story Points**: {SP}

## Resumen
- {cambios realizados}

## Tipo de cambio
- [x] {tipo marcado}

## Archivos clave modificados
- `{archivos}` — {descripcion}

## Como probar
1. `docker compose up --build -d`
2. {pasos de verificacion}

## Checklist
- [x] Codigo funcional sin errores
- [x] Tests escritos y pasando
- [x] Documentacion actualizada si aplica
- [x] Sin credenciales hardcodeadas

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

8. Retornar la URL del PR al usuario.

### Al hacer MERGE (solo si el usuario lo solicita)

9. Merge con squash para mantener historial limpio:
```bash
gh pr merge {PR-number} --squash --delete-branch
```

10. Volver a master:
```bash
git checkout master
git pull origin master
```
