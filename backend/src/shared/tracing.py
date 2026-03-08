"""OpenTelemetry tracing configuration."""
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
import logging

logger = logging.getLogger(__name__)

OTEL_ENABLED = os.getenv("OTEL_ENABLED", "true").lower() == "true"
SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "flight-api")


def setup_tracing(app, engine=None):
    """Configure OpenTelemetry tracing for the application."""
    if not OTEL_ENABLED:
        logger.info("OpenTelemetry tracing is disabled")
        return

    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "service.version": "1.0.0",
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    })

    provider = TracerProvider(resource=resource)

    # Export to console in development (replace with OTLP in production)
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        except Exception:
            logger.warning("OTLP exporter not available, falling back to console")
            exporter = ConsoleSpanExporter()
    else:
        exporter = ConsoleSpanExporter()

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app, excluded_urls="health,metrics")

    # Instrument SQLAlchemy
    if engine:
        SQLAlchemyInstrumentor().instrument(engine=engine)

    # Instrument Redis
    RedisInstrumentor().instrument()

    # Instrument Celery
    CeleryInstrumentor().instrument()

    logger.info(f"OpenTelemetry tracing enabled for {SERVICE_NAME}")
