# Errores Sprint 2 — Tests + Inicio Frontend

> Sprint 2: US-08 a US-15 | 33 SP | Completado 2026-03-06

---

## ERR-S2-01: Conflicto en conftest.py al mergear US-09 y US-10

**Severidad:** Alta
**US afectada:** US-09 (Tests Bookings), US-10 (Tests Auth)
**Recurrente:** Si → REC-01

### Descripcion
US-08, US-09 y US-10 corrieron en paralelo con worktree isolation. Los tres agents crearon `backend/tests/unit/conftest.py` independientemente con el mismo patron (mock de database + SQLite in-memory) pero con diferencias:
- US-08: mock de database con `type(sys)()`, imports de flights y bookings models
- US-09: mock con `types.ModuleType()`, agrego mocks de redis/celery/tasks
- US-10: mock similar a US-09, agrego `get_db` mock y auth model

Al mergear US-09 y US-10 (despues de US-08), ambas tenian conflictos add/add en conftest.py.

### Causa raiz
Patron REC-01: multiples agents creando el mismo archivo compartido (conftest.py) en paralelo. Identico al problema de main.py en Sprint 1.

### Solucion aplicada
Rebase manual para cada branch:
- US-09: se mantuvo conftest de HEAD (US-08) y se agregaron los mocks de redis/celery/tasks
- US-10: se mantuvo conftest de HEAD (US-08+09) y se agrego import de auth.models

### Leccion aprendida
Archivos de configuracion compartidos (conftest.py, main.py) deben identificarse antes de lanzar agents paralelos. Opciones:
1. Crear el archivo compartido ANTES de lanzar los agents
2. Asignar un solo agent para crear/modificar el archivo compartido
3. Usar el skill `resolve-parallel-conflicts.md` post-merge

---

## ERR-S2-02: Agent sobreescribio pyproject.toml completo

**Severidad:** Critica
**US afectada:** US-15 (Bandit CI)
**Recurrente:** Si → REC-03

### Descripcion
El agent de US-15 debio AGREGAR la seccion `[tool.bandit]` al `pyproject.toml` existente. En su lugar, creo un archivo nuevo con SOLO la config de bandit, eliminando toda la config de ruff, mypy, pytest y coverage (59 lineas perdidas).

### Contenido perdido
```toml
[project]                    # metadata del proyecto
[tool.ruff]                  # config de linting
[tool.ruff.lint]             # reglas de ruff
[tool.ruff.lint.isort]       # config de imports
[tool.mypy]                  # type checking
[tool.pytest.ini_options]    # pytest config + coverage addopts
[tool.coverage.run]          # coverage source/omit
[tool.coverage.report]       # coverage threshold 80%
```

### Causa raiz
El agent uso Write en vez de Edit para modificar pyproject.toml. Al usar Write, sobreescribio todo el contenido. Esto ocurrio porque:
1. El agent posiblemente no leyo el archivo completo antes de escribir
2. Las instrucciones del prompt no enfatizaron "usar Edit, NO Write"

### Solucion aplicada
Commit de fix post-merge restaurando el pyproject.toml completo con todas las secciones + bandit:
```
fix(config): restaurar pyproject.toml con ruff, mypy, pytest, coverage y bandit
```

### Prevencion
En las instrucciones de los agents, agregar explicitamente:
> "IMPORTANTE: Para modificar archivos existentes, usar SIEMPRE Edit (no Write). Leer el archivo completo primero."

---

## ERR-S2-03: Conflictos frontend al mergear US-14 tras US-12/13

**Severidad:** Alta
**US afectada:** US-14 (Dashboard Stats)
**Recurrente:** Si → REC-01

### Descripcion
US-12/13 y US-14 ambos crearon el frontend desde cero (Vite + React). US-14 necesitaba el scaffolding para que el DashboardPage.tsx existiera, asi que duplico toda la estructura. Al mergear US-14 despues de US-12/13, hubo conflictos en 6 archivos:
- `package.json`
- `App.tsx`
- `Layout.tsx`
- `DashboardPage.tsx`
- `LoginPage.tsx`
- `authStore.ts`

### Causa raiz
Patron REC-01 en su maxima expresion: un directorio completo (`frontend/`) creado desde cero por dos agents independientes. Solo DashboardPage.tsx era realmente diferente.

### Solucion aplicada
```bash
git checkout --ours frontend/package.json frontend/src/App.tsx \
  frontend/src/components/Layout.tsx frontend/src/pages/LoginPage.tsx \
  frontend/src/stores/authStore.ts
git checkout --theirs frontend/src/pages/DashboardPage.tsx
```
Solo se mantuvo el DashboardPage.tsx de US-14 (con stats completas) y el resto de US-12/13.

### Leccion aprendida
Cuando una US depende del scaffolding de otra, las opciones son:
1. **Secuencial**: ejecutar la US base primero, luego la dependiente
2. **Merge selectivo**: como se hizo aqui (--ours/--theirs)
3. **Branch desde branch**: US-14 partiendo del branch de US-12/13 (no de master)

---

## ERR-S2-04: Tabla users no existia en migracion Alembic

**Severidad:** Critica
**US afectada:** US-03 (Sprint 1, detectado en Sprint 2)

### Descripcion
Al levantar el proyecto y registrar un usuario, el endpoint `/auth/register` retornaba `Internal Server Error` con:
```
sqlalchemy.exc.ProgrammingError: relation "users" does not exist
```

### Causa raiz
Cuando se implemento US-03 (JWT Auth en Sprint 1), se creo el modelo `User` pero:
1. `alembic/env.py` no importaba `src.features.auth.models.User`
2. No se genero la migracion correspondiente con `alembic revision --autogenerate`
3. La migracion inicial (`001_initial_schema.py`) solo incluia destinations, flights y bookings

### Solucion aplicada
1. Agregar import en `alembic/env.py`:
   ```python
   from src.features.auth.models import User
   ```
2. Generar migracion:
   ```bash
   alembic revision --autogenerate -m "add users table"
   ```
3. Aplicar:
   ```bash
   alembic upgrade head
   ```

### Prevencion
El skill `new-feature.md` debe incluir un paso obligatorio:
> "Si el feature incluye nuevos modelos SQLAlchemy, actualizar `alembic/env.py` con el import del modelo y generar migracion."

---

## ERR-S2-05: Incompatibilidad passlib + bcrypt >= 4.1

**Severidad:** Critica
**US afectada:** US-03 (Sprint 1, detectado en Sprint 2)

### Descripcion
Al registrar un usuario, passlib crasheaba con:
```
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary
```

### Causa raiz
`passlib==1.7.4` no es compatible con `bcrypt >= 4.1`. La version 4.1+ de bcrypt cambio la API de `hashpw()` para rechazar passwords >72 bytes en la fase de deteccion de bugs internos de passlib (no en el hash real del usuario).

### Solucion aplicada
Pinear bcrypt a una version compatible en `requirements.txt`:
```
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
```

### Alternativas consideradas
- Migrar a `argon2-cffi` (mejor algoritmo pero requiere refactor)
- Usar `passlib[bcrypt]` con `PASSLIB_BUILTIN_BCRYPT=enabled` (fragil)
- Pin de bcrypt (elegida por ser la mas simple y segura)

---

## Resumen Sprint 2

| Categoria | Cantidad | Recurrentes |
|-----------|----------|-------------|
| Conflictos merge paralelo | 2 | Si (REC-01) |
| Agent sobreescribe archivo | 1 | Si (REC-03) |
| Migracion faltante | 1 | No (pero prevenible) |
| Dependencia incompatible | 1 | No |
| **Total** | **5** | **3** |
