# Skill: Add New API Endpoint

Add a new endpoint to an existing feature in the Flight Reservation System.

## Instructions

1. Ask the user: which feature (flights, bookings, ai), HTTP method, path, and what it should do
2. Determine if it's a read (Query) or write (Command) operation

### For Query (GET) endpoints:
- Add the query function in `src/features/{feature}/queries.py`
- Add the route in `src/api/v1/{feature}.py` with `@router.get()`
- Use `response_model` with the appropriate Pydantic schema

### For Command (POST/PUT/DELETE) endpoints:
- If needed, add a new Pydantic schema in `src/features/{feature}/schemas.py`
- Add the command function in `src/features/{feature}/commands.py`
- Add the route in `src/api/v1/{feature}.py`
- Wrap ValueError exceptions with `HTTPException(status_code=400)`
- If async processing needed, dispatch Celery task with `task.delay(json.dumps(payload))`

### Conventions:
- Routes use trailing slash: `/endpoint/`
- Response models are Pydantic schemas with `from_attributes=True`
- DB session via `db: Session = Depends(get_db)`
- All responses in Spanish
- Add a test in `tests/test_{feature}.py` or `tests/test_integration.py`

### Example pattern:
```python
@router.get("/{id}/", response_model=schemas.Flight)
def get_flight(id: int, db: Session = Depends(get_db)):
    result = queries.get_flight_by_id(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="No encontrado")
    return result
```
