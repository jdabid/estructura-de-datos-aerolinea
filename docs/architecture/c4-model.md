# Modelo C4 - Flight Reservation System

Diagramas arquitectónicos siguiendo el modelo C4 de Simon Brown.

---

## Nivel 1: Contexto del Sistema

Muestra el sistema de reservas y sus interacciones con usuarios y servicios externos.

```mermaid
graph TB
    User["👤 Usuario<br/><i>Pasajero o agente</i>"]
    Admin["👤 Administrador<br/><i>Equipo de operaciones</i>"]

    System["✈️ Flight Reservation System<br/><i>Sistema de reservas de vuelos<br/>FastAPI + PostgreSQL + Redis</i>"]

    Groq["☁️ Groq API<br/><i>LLM Llama 3.3 70B<br/>Servicio externo de IA</i>"]
    Monitoring["📊 Stack de Monitoreo<br/><i>Prometheus + Grafana + Jaeger</i>"]

    User -->|"Busca vuelos, crea reservas<br/>REST API / Chat IA"| System
    Admin -->|"Gestiona vuelos, consulta<br/>estadísticas y dashboards"| System
    System -->|"Inferencia LLM para<br/>agente conversacional"| Groq
    System -->|"Expone métricas y trazas"| Monitoring
    Admin -->|"Consulta dashboards<br/>y alertas"| Monitoring

    style System fill:#1168bd,stroke:#0b4884,color:#fff
    style Groq fill:#999,stroke:#666,color:#fff
    style Monitoring fill:#999,stroke:#666,color:#fff
```

---

## Nivel 2: Contenedores

Detalle de los contenedores que componen el sistema.

```mermaid
graph TB
    User["👤 Usuario"]
    Admin["👤 Administrador"]

    subgraph system["Flight Reservation System"]
        API["🌐 API Server<br/><i>FastAPI + Uvicorn<br/>Puerto 8000</i>"]
        Worker["⚙️ Celery Worker<br/><i>Procesamiento asíncrono<br/>Tareas en segundo plano</i>"]
        DB["🗄️ PostgreSQL 15<br/><i>Base de datos relacional<br/>+ pgvector</i>"]
        Redis["⚡ Redis 7<br/><i>Caché, contadores<br/>y resultados Celery</i>"]
        RabbitMQ["📨 RabbitMQ 3<br/><i>Message broker<br/>Cola de tareas</i>"]
        Frontend["🖥️ Frontend<br/><i>Interfaz web<br/>HTML/JS</i>"]
    end

    Groq["☁️ Groq API"]
    Prometheus["📊 Prometheus"]
    Jaeger["🔍 Jaeger"]

    User -->|"HTTPS"| Frontend
    User -->|"REST API"| API
    Admin -->|"REST API"| API
    Frontend -->|"HTTP/JSON"| API

    API -->|"SQLAlchemy<br/>TCP 5432"| DB
    API -->|"redis-py<br/>TCP 6379"| Redis
    API -->|"task.delay()"| RabbitMQ
    API -->|"HTTP/JSON<br/>LangChain"| Groq
    API -->|"/metrics"| Prometheus
    API -->|"OpenTelemetry<br/>trazas"| Jaeger

    RabbitMQ -->|"AMQP<br/>consume tasks"| Worker
    Worker -->|"SQLAlchemy<br/>TCP 5432"| DB
    Worker -->|"redis-py<br/>TCP 6379"| Redis

    style API fill:#1168bd,stroke:#0b4884,color:#fff
    style Worker fill:#1168bd,stroke:#0b4884,color:#fff
    style DB fill:#2d882d,stroke:#1a5c1a,color:#fff
    style Redis fill:#d94f00,stroke:#a33b00,color:#fff
    style RabbitMQ fill:#ff6600,stroke:#cc5200,color:#fff
    style Frontend fill:#438dd5,stroke:#2e6da4,color:#fff
```

---

## Nivel 3: Componentes (API Server)

Detalle interno del contenedor API con sus features y módulos compartidos.

```mermaid
graph TB
    subgraph api["API Server (FastAPI)"]
        subgraph routes["API Routes (src/api/v1/)"]
            FlightsAPI["✈️ flights.py<br/><i>CRUD de vuelos</i>"]
            BookingsAPI["📋 bookings.py<br/><i>Gestión de reservas</i>"]
            AIAPI["🤖 ai.py<br/><i>Chat con agente IA</i>"]
            AuthAPI["🔐 auth.py<br/><i>Registro y login JWT</i>"]
            StatsAPI["📊 stats.py<br/><i>Dashboard estadísticas</i>"]
        end

        subgraph features["Features (src/features/)"]
            Flights["✈️ flights/<br/><i>models, schemas<br/>commands, queries</i>"]
            Bookings["📋 bookings/<br/><i>models, schemas<br/>commands, queries</i>"]
            AI["🤖 ai/<br/><i>agent.py, tools.py<br/>LangChain ReAct</i>"]
            Auth["🔐 auth/<br/><i>models, schemas<br/>commands, queries</i>"]
            Stats["📊 stats/<br/><i>queries, schemas<br/>Redis counters</i>"]
        end

        subgraph shared["Shared (src/shared/)"]
            Database["🗄️ database.py<br/><i>SQLAlchemy engine<br/>+ get_db()</i>"]
            RedisClient["⚡ redis_client.py<br/><i>Conexión Redis<br/>helpers</i>"]
            Metrics["📈 metrics.py<br/><i>Prometheus<br/>instrumentación</i>"]
            Tracing["🔍 tracing.py<br/><i>OpenTelemetry<br/>configuración</i>"]
        end
    end

    FlightsAPI --> Flights
    BookingsAPI --> Bookings
    AIAPI --> AI
    AuthAPI --> Auth
    StatsAPI --> Stats

    Flights --> Database
    Bookings --> Database
    Bookings --> RedisClient
    Auth --> Database
    Stats --> RedisClient
    AI --> Flights
    AI --> Bookings

    DB["🗄️ PostgreSQL"]
    Redis["⚡ Redis"]
    Groq["☁️ Groq API"]

    Database --> DB
    RedisClient --> Redis
    AI -->|"LangChain"| Groq

    style api fill:#f5f5f5,stroke:#ccc
    style routes fill:#e8f4fd,stroke:#b8daff
    style features fill:#e8f5e9,stroke:#a5d6a7
    style shared fill:#fff3e0,stroke:#ffcc80
```

---

## Notas

- **Nivel 4 (Código)** no se incluye ya que el código fuente es la mejor documentación a ese nivel.
- Los diagramas se generan con [Mermaid](https://mermaid.js.org/) y se renderizan en GitHub/GitLab.
- Para visualizar localmente: usar extensión Mermaid de VS Code o [mermaid.live](https://mermaid.live).
