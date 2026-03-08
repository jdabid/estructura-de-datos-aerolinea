import os
from celery import Celery

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
broker_url = os.getenv("RABBITMQ_URL", "pyamqp://admin:admin123@localhost:5672//")

celery_app = Celery(
    "worker",
    broker=broker_url,
    backend=f"redis://{redis_host}:{redis_port}/0",
    include=["src.worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    # Dead Letter Queue
    task_reject_on_worker_lost=True,
    task_default_queue="default",
    task_queues={
        "default": {
            "exchange": "default",
            "routing_key": "default",
        },
        "dead_letter": {
            "exchange": "dead_letter",
            "routing_key": "dead_letter",
        },
    },
    task_routes={
        "process_booking_event": {"queue": "default"},
    },
)