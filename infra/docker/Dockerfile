# Stage 1: Build dependencias
FROM python:3.11-slim as builder
WORKDIR /install
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Imagen Final
FROM python:3.11-slim
WORKDIR /app

# Crear usuario de sistema para seguridad
RUN addgroup --system appgroup && adduser --system --group appuser

# Copiar solo librerías instaladas y el código
COPY --from=builder /install /usr/local
COPY ./src ./src

# Permisos de ejecución
RUN chown -R appuser:appgroup /app
USER appuser

ENV PYTHONPATH=/app
EXPOSE 8000

# Healthcheck para Kubernetes
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]