# Skill: Create New Vertical Slice Feature

Create a new feature following the Vertical Slice Architecture + CQRS pattern used in this project.

## Instructions

1. Ask the user for: feature name, model fields, and business rules
2. Create the following files in order:

### `src/features/{name}/models.py`
- Import `Column`, types from `sqlalchemy` and `Base` from `src.shared.database`
- Define SQLAlchemy model with `__tablename__`
- Add relationships if needed

### `src/features/{name}/schemas.py`
- Import `BaseModel`, `ConfigDict`, `field_validator` from pydantic
- Create `{Name}Base` with fields and validators
- Create `{Name}Create(Base)` for input
- Create `{Name}({Name}Base)` with `model_config = ConfigDict(from_attributes=True)` and `id: int`

### `src/features/{name}/commands.py`
- Import `Session` from sqlalchemy.orm and local models/schemas
- Create functions for write operations (create, update, delete)
- Follow pattern: receive db session + schema, create model instance, commit, refresh, return

### `src/features/{name}/queries.py`
- Import `Session` from sqlalchemy.orm and local models
- Create functions for read operations (get_all, get_by_id, filters)
- Follow pattern: `db.query(Model).filter(...).all()`

### `src/api/v1/{name}.py`
- Import `APIRouter`, `Depends`, `HTTPException` from fastapi
- Import `get_db` from `src.shared.database`
- Import feature commands, queries, schemas
- Create router with `prefix="/{name}"` and `tags=["{name}"]`
- Add POST and GET endpoints
- Use `Depends(get_db)` for session injection
- Catch `ValueError` in POST and return HTTP 400

### Register in `src/main.py`
- Add `from src.api.v1 import {name}`
- Add `app.include_router({name}.router, prefix="/api/v1")`

### `tests/test_{name}.py`
- Import TestClient, app, Base, engine
- Add `clean_db` fixture (drop_all, create_all, yield, drop_all)
- Write at least 2 tests: happy path and validation error

3. If the feature needs async processing, add a Celery task in `src/worker/tasks.py`
4. If the feature needs Redis stats, add helpers using `update_stat` and `log_to_list` from `src.shared.redis_client`
