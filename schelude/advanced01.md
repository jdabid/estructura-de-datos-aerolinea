### Fase 1: Base e Infraestructura - Detalle de Implementación

Para cumplir con el entregable de la **Semana 1**, como DevOps y Python Developer, aquí tienes el desglose técnico de todo lo que necesitamos configurar para establecer una base sólida y escalable.

---

### 1. Herramientas y Requisitos Previos
Antes de iniciar, el equipo de desarrollo debe contar con:
*   **Python 3.11+**: Motor principal del backend.
*   **Docker & Docker Compose**: Para contenedores y orquestación local.
*   **kubectl & Helm**: Para la gestión de Kubernetes.
*   **Kind o Minikube**: Para simular el clúster de K8s localmente.
*   **Git**: Control de versiones.

---

### 2. Estructura de Proyecto (Repositorio)
Basado en la arquitectura de **Vertical Slices**, inicializaremos el repositorio con la siguiente estructura:

```text
/flight-reservation-system
├── src/
│   ├── api/                # Entrypoints de FastAPI
│   ├── features/           # Slices (vacíos por ahora)
│   ├── shared/             # Utilidades comunes
│   └── main.py             # Inicialización de la App
├── infra/
│   ├── docker/
│   │   └── Dockerfile      # Multi-stage build
│   ├── k8s/
│   └── helm/
│       └── flight-app/     # Chart de Helm
├── .github/workflows/      # CI/CD (GitHub Actions)
├── docker-compose.yml      # Entorno de desarrollo local
├── pyproject.toml          # Dependencias (Poetry/Pip)
└── .gitignore
```

---

### 3. Dockerización: Multi-stage Build
Para optimizar las imágenes (seguridad y peso), usaremos un `Dockerfile` de dos etapas:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
# Copiamos solo lo necesario del builder
COPY --from=builder /root/.local /root/.local
COPY ./src ./src
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 4. Entorno Local con `docker-compose`
Este archivo levantará todos los servicios necesarios para que el desarrollador trabaje sin instalar nada localmente (excepto Docker).

```yaml
version: '3.8'
services:
  api:
    build: 
      context: .
      dockerfile: infra/docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/flights
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: flights
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
```

---

### 5. Esqueleto de Kubernetes con Helm
Crearemos un Chart de Helm básico para desplegar en K8s. Lo mínimo necesario es:

*   **`Chart.yaml`**: Metadatos del proyecto.
*   **`values.yaml`**: Variables de configuración (réplicas, tags de imagen).
*   **`templates/`**:
    *   `deployment.yaml`: Definición de los pods del API.
    *   `service.yaml`: Exposición del API.
    *   `configmap.yaml`: Variables de entorno no sensibles.

---

### 6. CI/CD Inicial (GitHub Actions)
Configuraremos un workflow (`.github/workflows/main.yml`) que se ejecute en cada *Push* o *PR*:

1.  **Linting**: Revisión de estilo con `flake8` o `ruff`.
2.  **Tests**: Ejecución de `pytest` (aunque inicialmente sean pocos).
3.  **Build Check**: Verificar que la imagen de Docker construye correctamente.

---

### 7. Archivos de Configuración Base
*   **.gitignore**: Ignorar `__pycache__`, `.env`, `.venv`, y carpetas de IDEs.
*   **requirements.txt / pyproject.toml**: Incluir `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic` y `psycopg2-binary`.

**Con esto cerramos la Semana 1**, dejando el "terreno preparado" para que en la Semana 2 empecemos a codificar el primer slice funcional de vuelos sin preocuparnos por la infraestructura.