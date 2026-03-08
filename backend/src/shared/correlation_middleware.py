"""Middleware to generate and propagate correlation IDs."""
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.shared.logging_config import correlation_id_var
import logging

logger = logging.getLogger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Generate or extract correlation ID for each request."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Get correlation ID from header or generate new one
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            request.headers.get("X-Request-ID", str(uuid.uuid4()))
        )

        # Set in context var for logging
        token = correlation_id_var.set(correlation_id)

        try:
            logger.info(
                "Request started",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "correlation_id": correlation_id,
                },
            )

            response = await call_next(request)

            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id

            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "correlation_id": correlation_id,
                },
            )

            return response
        finally:
            correlation_id_var.reset(token)
