# Skill: Run Tests

Run tests for the Flight Reservation System and diagnose failures.

## Instructions

1. Check if Docker services are running:
```bash
docker compose ps
```

2. If services are up, run tests inside the API container:
```bash
docker compose exec api pytest tests/ -v --tb=short
```

3. If services are NOT up, run tests locally (requires PostgreSQL and Redis running):
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/flights REDIS_HOST=localhost RABBITMQ_URL="" PYTHONPATH=. pytest tests/ -v --tb=short
```

4. After running tests, restart the API to recreate tables:
```bash
docker compose restart api
```

5. If tests fail:
   - Read the failing test file
   - Read the relevant source code (commands, queries, schemas)
   - Check if the business logic matches the test expectations
   - Fix the issue and re-run

6. To run a specific test:
```bash
docker compose exec api pytest tests/test_integration.py::test_full_booking_flow -v
```
