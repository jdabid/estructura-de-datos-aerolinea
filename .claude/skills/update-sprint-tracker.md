# Skill: Update Sprint Tracker

Actualiza automaticamente el archivo `evaluacion-tecnica/cronograma-sprints.md` cada vez que se finaliza una User Story.

## Trigger
Este skill se ejecuta AUTOMATICAMENTE como parte del skill `finish-user-story`, justo ANTES de hacer el push y crear el PR.

## Instructions

1. Leer `evaluacion-tecnica/cronograma-sprints.md`

2. Actualizar la fila de la US completada en la tabla del Sprint correspondiente:
   - Cambiar Estado de `PENDIENTE` a `DONE`
   - Agregar el nombre del branch
   - Agregar el link al PR: `[#N](https://github.com/jdabid/flight-reservation-system/pull/N)`
   - Agregar la fecha actual (YYYY-MM-DD)

3. Recalcular las metricas del Sprint:
   - Sumar los SP de todas las US con estado DONE en ese sprint
   - Actualizar `SP Completados: X/Y`
   - Actualizar la barra de progreso del sprint:
     ```
     Sprint N: [####__________] XX%  (X/Y SP)
     ```
     - Cada `#` representa ~2.5% (40 caracteres total)
     - Calcular: chars = round(porcentaje / 100 * 38)
   - Si todas las US del sprint estan DONE, cambiar Estado a `COMPLETADO`

4. Recalcular las metricas globales (seccion "Resumen General"):
   - Contar US completadas, en progreso y pendientes de TODOS los sprints
   - Sumar SP completados de TODOS los sprints
   - Calcular SP restantes = 229 - SP completados
   - Actualizar velocidad actual = SP completados del sprint actual
   - Actualizar barra de progreso global:
     ```
     Completado: [####______] XX%  (X/229 SP)
     ```
   - Actualizar "Ultima actualizacion" con fecha actual

5. Actualizar el Burndown Chart:
   - Marcar el punto actual con `← actual` en el SP restante mas cercano

6. Agregar entrada al Historial de Cambios al final de la tabla:
   ```
   | YYYY-MM-DD | US-XX | COMPLETADA | N | {herramientas usadas} |
   ```
   Herramientas posibles:
   - Skill: start-user-story, finish-user-story, git-workflow
   - Skill: new-feature, new-endpoint, new-celery-task, ai-tool
   - Skill: run-tests, docker-ops
   - Agent (worktree isolation)
   - Agent (general-purpose)
   - MCP (postgres)

7. Si una US cambia a EN PROGRESO (se inicio pero no se termino):
   - Cambiar Estado de `PENDIENTE` a `EN PROGRESO`
   - Agregar el nombre del branch
   - No agregar PR ni fecha

## Ejemplo de actualizacion

### Antes:
```
| US-04 | Sistema de excepciones centralizado | 5 | PENDIENTE | — | — | — |
```

### Despues:
```
| US-04 | Sistema de excepciones centralizado | 5 | DONE | `feature/s1-US04-excepciones` | [#16](https://github.com/jdabid/flight-reservation-system/pull/16) | 2026-03-07 |
```

## Notas del Sprint
Opcionalmente, agregar una nota relevante en la seccion "Notas del Sprint N":
- Si se uso paralelismo (agents)
- Si hubo conflictos de merge
- Si se cambio el scope de la US
- Si se bloqueo por dependencias
