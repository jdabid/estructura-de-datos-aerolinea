# Skill: Finish User Story

Finaliza una User Story: commit final, push, creacion de PR y opcionalmente merge.

## Instructions

1. Verificar el estado actual del branch:
```bash
git branch --show-current
git status
git log --oneline -5
```

2. Si hay cambios sin commitear:
   - Revisar los archivos modificados
   - Confirmar con el usuario que archivos incluir
   - Hacer commit siguiendo Conventional Commits (ver `git-workflow.md`)
   - NUNCA usar `git add .` — agregar archivos especificos

3. Push de la branch:
```bash
git push -u origin $(git branch --show-current)
```

4. Extraer informacion de la User Story:
   - Parsear el nombre del branch para obtener sprint y US-ID
   - Consultar `evaluacion-tecnica/cronograma-scrum.md` para SP y descripcion
   - Recopilar los commits de la branch para el resumen

5. Crear el Pull Request con el template estandar:
```bash
gh pr create --title "[US-{ID}] {tipo}: {descripcion}" --body "$(cat <<'EOF'
## User Story
**US-{ID}**: {descripcion completa}
**Sprint**: {N}
**Story Points**: {SP}

## Resumen
{lista de cambios basada en los commits de la branch}

## Tipo de cambio
- [x] {tipo correspondiente}

## Archivos clave modificados
{lista de archivos con descripcion de cada cambio}

## Como probar
1. `docker compose up --build -d`
2. {pasos especificos de verificacion}
3. {resultado esperado}

## Checklist
- [x] Codigo funcional sin errores
- [x] Tests escritos y pasando
- [x] Documentacion actualizada si aplica
- [x] Sin credenciales hardcodeadas
- [x] Sin archivos innecesarios

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

6. Mostrar la URL del PR al usuario.

7. Preguntar si desea hacer merge:
   - Si: ejecutar squash merge y volver a master
   ```bash
   gh pr merge {PR-number} --squash --delete-branch
   git checkout master
   git pull origin master
   ```
   - No: dejar el PR abierto para review
