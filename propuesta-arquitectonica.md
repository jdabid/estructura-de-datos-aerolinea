### Propuesta Técnica y Arquitectónica: Sistema de Reservas de Vuelo

Presento la siguiente propuesta para el desarrollo y despliegue del sistema de reservas de la aerolínea, siguiendo los requerimientos solicitados. (enunciato.txt)

### 1. Stack Tecnológico Definido

*   **Backend:** Python 3.11+ con **FastAPI** (por su alto rendimiento, soporte nativo de asincronía y facilidad para implementar CQRS).
*   **Base de Datos Principal:** **PostgreSQL** (Relacional para manejar transacciones de vuelos y reservas).
*   **Caché y Mensajería Rápida:** **Redis** (Para caching de destinos frecuentes y como broker secundario).
*   **Broker de Mensajería:** **RabbitMQ** (Para la comunicación asíncrona entre servicios y procesamiento de tareas pesadas).
*   **Procesamiento en Segundo Plano:** **Celery** o **TaskIQ** (Para el cálculo de reportes complejos y envío de correos/dulces virtuales).
*   **IA:** **LangChain** + **OpenAI API** o **Llama 3** (local) para análisis de sentimientos y recomendaciones.

### 2. Patrón Arquitectónico: Vertical Slice + CQRS

Se abandonará la arquitectura tradicional por capas en favor de **Vertical Slice Architecture**, donde cada funcionalidad (slice) es independiente. Dentro de cada slice, aplicaremos **CQRS** (Command Query Responsibility Segregation).

*   **Commands:** Encargados de las acciones que cambian el estado (ej. `CrearReserva`, `RegistrarImpuestoPorDestino`).
*   **Queries:** Encargados de las consultas de lectura (ej. `ObtenerTotalRecaudado`, `ConsultarImpuestoPorCiudad`).

Esto permite que los reportes solicitados (recaudo, destino preferido, etc.) sean consultas optimizadas que no interfieran con la lógica de creación de reservas.

### 3. Estructura de Carpetas Propuesta

```text
/flight-reservation-system
│
├── src/
│   ├── api/                # Puntos de entrada (FastAPI Routes)
│   ├── features/           # Vertical Slices
│   │   ├── bookings/       # Slice de Reservas
│   │   │   ├── commands/   # Lógica de escritura
│   │   │   ├── queries/    # Lógica de lectura
│   │   │   └── models.py
│   │   ├── flights/        # Slice de Gestión de Vuelos
│   │   └── reports/        # Slice de Reportes (Recaudos, Mascotas, Infantes)
│   ├── shared/             # Código común (Excepciones, Utilidades)
│   ├── worker/             # Consumidores de RabbitMQ (Celery tasks)
│   └── main.py
│
├── infra/
│   ├── docker/             # Dockerfiles (dev, prod)
│   ├── k8s/                # Manifiestos base de Kubernetes
│   │   └── kustomize/      # Configuraciones por entorno (dev, prod)
│   └── helm/               # Charts de Helm para empaquetado
│
├── tests/                  # Pruebas unitarias y de integración
├── pyproject.toml          # Dependencias y configuración de Python
└── README.md
```

### 4. Dockerización y Orquestación

*   **Docker:** Se utilizarán *multi-stage builds* para optimizar el tamaño de la imagen de Python, separando las dependencias de compilación de la imagen de ejecución.
*   **Kubernetes (K8s):** Despliegue mediante `Deployments` para el API y los Workers, y `StatefulSets` para Redis/RabbitMQ (si se gestionan internamente).
*   **Helm:** Se creará un Chart para empaquetar toda la aplicación, permitiendo gestionar versiones y dependencias de forma sencilla.
*   **Kustomize:** Se usará para sobrescribir configuraciones específicas (variables de entorno, réplicas) según el ambiente sin duplicar el código de Helm.

### 5. Message Queue & Background Processing

*   **Flujo:** Cuando se realiza una reserva, el API publica un evento en **RabbitMQ**.
*   **Procesamiento:** Un worker de Celery consume el evento para:
    1. Actualizar las estadísticas de "destino preferido" en **Redis**.
    2. Calcular los impuestos complejos de forma asíncrona.
    3. Registrar el costo de los dulces si el pasajero es un infante (< 12 años).
*   **Redis:** Se utiliza para almacenar los resultados de los reportes más consultados (ej. Total recaudado) para que la respuesta sea instantánea.

### 6. Propuesta para el Manejo de IA

Se propone implementar un **Agente de Inteligencia Artificial** integrado en el backend para:

1.  **Predicción de Demanda y Precios Dinámicos:** Utilizar un modelo de regresión (Scikit-learn) o una integración con LLMs para sugerir el ajuste de impuestos o descuentos (como el de promoción del 10%) basado en la popularidad del destino.
2.  **Asistente de Reservas (Chatbot):** Un agente basado en RAG (Retrieval-Augmented Generation) que permita a los usuarios preguntar: *"¿Cuánto pagaría de impuestos si viajo a San Andrés con mi mascota?"*.
3.  **Análisis de Preferencias:** Procesar los datos de destinos para predecir tendencias de viaje estacionales y optimizar la compra de dulces para los infantes.

### 7. Resolución de Requerimientos del Enunciado

*   **Impuestos por destino:** Gestionado vía Command en el slice de `flights`.
*   **Mascotas y Promociones:** Lógica de cálculo inyectada en el comando `CrearReserva` (Precio * 0.90 si es promoción + Impuesto).
*   **Infantes (Dulces):** Lógica que detecta edad <= 12 años y dispara un evento asíncrono para contabilidad de dulces.
*   **Reportes:** Queries especializadas en el slice de `reports` que consumen datos agregados desde la base de datos o caché de Redis.