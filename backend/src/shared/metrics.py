from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator

# Custom metrics
BOOKINGS_TOTAL = Counter(
    "bookings_total",
    "Total number of bookings created",
    ["destination"],
)

BOOKING_PRICE = Histogram(
    "booking_price_dollars",
    "Distribution of booking prices",
    buckets=[50, 100, 200, 300, 500, 1000],
)

ACTIVE_REQUESTS = Gauge(
    "active_requests",
    "Number of active HTTP requests",
)

AI_REQUESTS_TOTAL = Counter(
    "ai_requests_total",
    "Total AI agent requests",
    ["endpoint"],
)

AI_RESPONSE_TIME = Histogram(
    "ai_response_time_seconds",
    "AI agent response time",
    buckets=[0.5, 1, 2, 5, 10, 30],
)

CELERY_TASKS_TOTAL = Counter(
    "celery_tasks_total",
    "Total Celery tasks processed",
    ["task_name", "status"],
)


def setup_metrics(app):
    """Configure Prometheus metrics for FastAPI."""
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        excluded_handlers=["/metrics", "/health"],
    ).instrument(app).expose(app, endpoint="/metrics")
