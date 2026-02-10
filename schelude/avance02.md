### Fase 2: Gestión de Vuelos - Implementación Técnica

En esta fase, implementaremos el **Vertical Slice** de `flights`. Siguiendo la arquitectura propuesta, separaremos la lógica de escritura (Commands) de la de lectura (Queries) y configuraremos el modelado en PostgreSQL para gestionar tanto los vuelos como los impuestos por destino.

A continuación, los archivos para crear la estructura y funcionalidad:

---

### 1. Configuración de Base de Datos
**Archivo:** `src/shared/database.py`
Este archivo gestiona la conexión con PostgreSQL utilizando SQLAlchemy.

```python

```

---

### 2. Modelos de Datos (PostgreSQL)
**Archivo:** `src/features/flights/models.py`
Definimos las tablas de `Destination` (donde viven los impuestos) y `Flight`.

```python

```

---

### 3. Schemas (Validación de Datos)
**Archivo:** `src/features/flights/schemas.py`
Usamos Pydantic para definir cómo entran y salen los datos de la API.

```python

```

---

### 4. Lógica de Negocio (CQRS: Commands & Queries)

**Archivo (Commands):** `src/features/flights/commands.py`
Lógica para crear/actualizar datos (Escritura).

```python

```

**Archivo (Queries):** `src/features/flights/queries.py`
Lógica para consultar datos (Lectura).

```python

```

---

### 5. API Endpoints (FastAPI)
**Archivo:** `src/api/v1/flights.py`

```python

```

---

### 6. Inicialización de la Aplicación
**Archivo:** `src/main.py`
Aquí unimos todo y nos aseguramos de que las tablas se creen al iniciar (en un entorno real usaríamos Alembic).

```python

```

### Resumen de lo entregado:
1.  **Modelado relacional:** Tablas para destinos (con impuestos) y vuelos.
2.  **CRUD completo:** Endpoints para crear y listar ambos recursos.
3.  **Arquitectura Limpia:** Separación de responsabilidades entre modelos, esquemas y lógica de negocio.
4.  **Inyección de Dependencias:** Gestión de sesiones de DB optimizada para FastAPI.

**Próximo paso (Semana 3):** Implementación de Reservas, donde usaremos los impuestos y promociones definidos aquí para calcular los precios finales.