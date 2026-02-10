### Fase 6: QA y Despliegue - Implementación Final

En esta última fase, cerramos el ciclo de desarrollo asegurando la calidad del código mediante **pruebas de integración**, optimizando la **imagen de producción** para seguridad y velocidad, y definiendo la infraestructura como código (IaC) necesaria para un despliegue escalable en **Kubernetes**.

---

### 1. Pruebas de Integración (QA)
**Archivo:** `tests/test_integration.py`  
Probamos el flujo completo: Crear destino -> Crear vuelo -> Crear reserva (validando impuestos y descuentos).

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_full_booking_flow():
    # 1. Crear un destino con promoción e impuestos
    dest_resp = client.post("/api/v1/flights/destinations/", json={
        "name": "Cartagena",
        "tax_amount": 50.0,
        "is_promotion": True,
        "allows_pets": True
    })
    assert dest_resp.status_code == 200
    dest_id = dest_resp.json()["id"]

    # 2. Crear un vuelo para ese destino
    flight_resp = client.post("/api/v1/flights/", json={
        "flight_number": "CT-123",
        "origin": "Bogotá",
        "base_price": 1000.0,
        "destination_id": dest_id
    })
    assert flight_resp.status_code == 200
    flight_id = flight_resp.json()["id"]

    # 3. Realizar una reserva (Debería aplicar 10% desc + 50 de impuesto)
    # 1000 * 0.9 = 900 + 50 = 950
    booking_resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Juan Perez",
        "passenger_age": 30,
        "has_pet": True,
        "flight_id": flight_id
    })
    assert booking_resp.status_code == 200
    assert booking_resp.json()["total_price"] == 950.0

def test_pet_validation_error():
    # Intentar reservar con mascota en destino que no permite
    client.post("/api/v1/flights/destinations/", json={
        "name": "Londres", "tax_amount": 100, "allows_pets": False
    })
    # ... asumiendo que el ID es 2
    client.post("/api/v1/flights/", json={
        "flight_number": "LON-99", "origin": "Bog", "base_price": 2000, "destination_id": 2
    })
    
    resp = client.post("/api/v1/bookings/", json={
        "passenger_name": "Mascota Lover", "passenger_age": 25, "has_pet": True, "flight_id": 2
    })
    assert resp.status_code == 400
    assert "no acepta mascotas" in resp.json()["detail"]
```

---

### 2. Dockerfile de Producción (Optimizado)
**Archivo:** `infra/docker/Dockerfile`  
Implementación de seguridad (usuario no-root) y reducción de peso.

```dockerfile
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
```

---

### 3. Orquestación: Helm Chart (Producción)
**Archivo:** `infra/helm/flight-app/templates/deployment.yaml`  
Configuración con auto-escalado y monitoreo.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-api
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: flight-api
  template:
    metadata:
      labels:
        app: flight-api
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      containers:
      - name: api
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 8000
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 200m
            memory: 256Mi
        envFrom:
        - configMapRef:
            name: {{ .Release.Name }}-config
        - secretRef:
            name: {{ .Release.Name }}-secrets
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flight-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ .Release.Name }}-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

### 4. CI/CD: Pipeline de Despliegue
**Archivo:** `.github/workflows/deploy.yml`

```yaml
name: CI/CD Pipeline
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env: {POSTGRES_PASSWORD: pass, POSTGRES_DB: flights}
        ports: [5432:5432]
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          pip install -r requirements.txt pytest httpx
          pytest tests/

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Build Docker Image
        run: |
          docker build -t myregistry/flight-app:latest -f infra/docker/Dockerfile .
          # docker push myregistry/flight-app:latest

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to K8s via Helm
        run: |
          helm upgrade --install flight-system ./infra/helm/flight-app \
            --set image.tag=latest \
            --namespace production
```

---

### 5. Documentación y Monitoreo (README Final)
**Archivo:** `README.md`

```markdown
# Flight Reservation System MVP

## Arquitectura
- **Backend:** FastAPI (Vertical Slices + CQRS).
- **Asincronía:** RabbitMQ + Celery para reportes y contabilidad de dulces.
- **IA:** Agente RAG con LangChain para sugerencia de precios.
- **Infra:** Docker Multi-stage y Kubernetes (Helm).

## Cómo ejecutar localmente
1. Clonar el repositorio.
2. Crear un archivo `.env` con `DATABASE_URL` y `OPENAI_API_KEY`.
3. Ejecutar `docker-compose up --build`.
4. Acceder a `http://localhost:8000/docs` para la documentación interactiva.

## Monitoreo
- **Métricas:** Los pods de K8s están anotados para ser scrapeados por **Prometheus**.
- **Dashboard:** Se incluye un template de **Grafana** en `infra/monitoring/` para visualizar:
  - Total Recaudado (vía Redis).
  - Uso de CPU/RAM por pod.
  - Tasa de error de reservas.
```

### Resumen Final del Proyecto:
1.  **Código Robusto:** Flujo completo desde la infraestructura hasta la IA.
2.  **Preparado para Prod:** Dockerfiles optimizados y manifiestos de K8s con HPA.
3.  **Calidad:** Suite de pruebas que garantiza que las reglas de negocio (mascotas, impuestos, promociones) no se rompan.
4.  **Visibilidad:** Sistema listo para ser monitoreado con herramientas estándar de la industria.

¡Con esto completamos el ciclo de 6 semanas y el sistema está listo para producción! 🚀