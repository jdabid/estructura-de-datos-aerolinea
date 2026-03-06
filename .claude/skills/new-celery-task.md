# Skill: Create New Celery Task

Add a new asynchronous task processed by the Celery worker.

## Instructions

1. Ask the user: task name, what data it processes, and what it should do

2. Add the task in `src/worker/tasks.py` following this pattern:

```python
@celery_app.task(
    name="{task_name}",
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def {task_name}(self, data: str):
    try:
        payload = json.loads(data)
        # Process the data
        # Use update_stat() for Redis counters
        # Use log_to_list() for Redis logs
        return f"Task {task_name} completed"
    except Exception as exc:
        logger.exception("Error in {task_name}")
        raise self.retry(exc=exc)
```

3. Key conventions:
   - Import `celery_app` from `.celery_app`
   - Import `update_stat`, `log_to_list` from `src.shared.redis_client`
   - Task data is always a JSON string (serialize with `json.dumps()`)
   - Use `bind=True` to access `self` for retries
   - Always wrap in try/except with `self.retry(exc=exc)`
   - Max 3 retries with 10s delay between attempts

4. To dispatch the task from a command:
```python
from src.worker.tasks import {task_name}
{task_name}.delay(json.dumps(payload))
```

5. Wrap the dispatch in try/except to not fail the main operation:
```python
try:
    {task_name}.delay(json.dumps(payload))
except Exception:
    logger.exception("Failed to dispatch {task_name}")
```

6. If the task needs to be registered, ensure it's importable from `src.worker.tasks` (already included in celery_app config).

7. Restart the worker after adding:
```bash
docker compose restart worker
```
