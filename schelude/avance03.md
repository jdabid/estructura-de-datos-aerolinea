### Fase 3: Reservas y CQRS - Implementación Técnica

En esta semana, implementaremos el vertical slice de **Reservas (`bookings`)**. Este componente es el corazón del sistema, ya que aquí es donde se aplica la lógica de negocio principal: validación de mascotas, aplicación de descuentos por promoción y cálculo de impuestos.

Siguiendo el patrón **CQRS**, hemos separado las acciones que modifican el estado (Commands) de las que solo consultan datos (Queries).

---

### 1. Actualización en el Slice de Vuelos (Soporte para Validación)
Para que la validación de mascotas sea funcional, actualizamos los modelos de `flights` para incluir el campo `allows_pets`.

**Archivo:** `src/features/flights/models.py` (Actualizado)
```python

    allows_pets = Column(Boolean, default=True)  # Nuevo campo para validación


```

---

### 2. Modelado de Reservas
**Archivo:** `src/features/bookings/models.py`
```python

```

---

### 3. Schemas de Validación
**Archivo:** `src/features/bookings/schemas.py`
```python

```

---

### 4. Lógica de Negocio (CQRS: Commands & Queries)

**Archivo (Commands):** `src/features/bookings/commands.py`
Aquí reside la lógica de cálculo: **Precio Base - 10% (si es promo) + Impuesto**.

```python

```

**Archivo (Queries):** `src/features/bookings/queries.py`
```python

```

---

### 5. API Endpoints
**Archivo:** `src/api/v1/bookings.py`
```python

```

---

### 6. Actualización de la Aplicación Principal
**Archivo:** `src/main.py`
Registramos el nuevo router de reservas.

```python
app.include_router(bookings.router, prefix="/api/v1")
```

### Resumen de Logros en la Semana 3:
1.  **Cálculo Dinámico:** Implementada la lógica de descuentos del 10% y aplicación de impuestos por destino.
2.  **Validación de Reglas:** El sistema ahora rechaza reservas con mascotas si el destino no las permite.
3.  **Arquitectura CQRS:** Separación clara entre la creación de la reserva y la consulta de las mismas.
4.  **Integridad de Datos:** Relación establecida entre Reservas y Vuelos para garantizar consistencia.

**Próximo paso (Semana 4):** Integraremos RabbitMQ y Celery para que, al detectar un pasajero infante (`passenger_age < 12`), se dispare automáticamente el proceso de "contabilidad de dulces" de forma asíncrona.