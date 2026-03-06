# Skill: Start User Story

Inicia el desarrollo de una User Story creando la branch, configurando el entorno y preparando el flujo de trabajo.

## Instructions

1. Pedir al usuario el ID de la User Story (ej: US-03) y el sprint (ej: S1)

2. Consultar el cronograma Scrum en `evaluacion-tecnica/cronograma-scrum.md` para obtener:
   - Descripcion de la user story
   - Story points
   - Criterio de aceptacion
   - Epica a la que pertenece

3. Determinar el tipo de branch segun la user story:
   - `feature/` para nuevas funcionalidades
   - `fix/` para correcciones
   - `refactor/` para reestructuracion
   - `test/` para tests
   - `docs/` para documentacion
   - `infra/` para Docker, K8s, Helm, CI/CD, Terraform
   - `chore/` para mantenimiento

4. Ejecutar la secuencia de inicio:

```bash
# Asegurar que master esta actualizado
git checkout master
git pull origin master

# Crear branch para la US
git checkout -b {tipo}/{sprint}-{US-ID}-{descripcion-corta}
```

5. Mostrar al usuario un resumen:
```
--- User Story Iniciada ---
Branch:    {nombre-branch}
US:        {US-ID} — {descripcion}
Sprint:    {sprint}
SP:        {story points}
Criterio:  {criterio de aceptacion}
---
```

6. Consultar el skill correspondiente segun el tipo de trabajo:
   - Si es un nuevo feature → seguir `new-feature.md`
   - Si es un nuevo endpoint → seguir `new-endpoint.md`
   - Si es una celery task → seguir `new-celery-task.md`
   - Si es una AI tool → seguir `ai-tool.md`
   - Si es tests → seguir `run-tests.md`
   - Si es Docker/K8s → seguir `docker-ops.md`

7. Durante el desarrollo, seguir las convenciones de `git-workflow.md` para commits.

8. Al finalizar, preguntar al usuario si quiere:
   - Hacer push y crear PR (seguir `git-workflow.md` seccion PR)
   - Solo hacer push sin PR
   - Seguir trabajando en la branch
