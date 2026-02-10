### Fase 4: Eventos y Workers - Implementación Técnica

En esta fase, integramos **RabbitMQ** y **Celery** para manejar procesos en segundo plano. Esto permite que la creación de reservas sea instantánea, mientras que las tareas administrativas y de analítica (como la contabilidad de dulces y estadísticas de recaudación) se ejecutan de forma asíncrona.

También utilizaremos **Redis** no solo como backend de Celery, sino como una base de datos en memoria para obtener reportes de alto rendimiento en tiempo real.

---

### 1. Cliente de Redis (Compartido)
**Archivo:** `src/shared/redis_client.py`
Este cliente centraliza la conexión a Redis para actualizar estadísticas.

```python

```

---

### 2. Configuración de Celery
**Archivo:** `src/worker/celery_app.py`
Configuramos Celery para usar RabbitMQ como broker de mensajes.

```python

```

---

### 3. Definición de Tareas Asíncronas
**Archivo:** `src/worker/tasks.py`
Aquí implementamos la lógica de los dulces y la actualización de estadísticas.

```python

```

---

### 4. Integración en el Command de Reservas
**Archivo:** `src/features/bookings/commands.py` (Actualizado)
Modificamos el comando para disparar el evento tras guardar la reserva en la DB.

```python

    
    # --- SEMANA 4: DISPARO DE EVENTO ASÍNCRONO ---
    payload = {
        "id": db_booking.id,
        "passenger_name": db_booking.passenger_name,
        "passenger_age": db_booking.passenger_age,
        "total_price": db_booking.total_price,
        "destination_name": destination.name
    }
    process_booking_event.delay(json.dumps(payload))
    # ---------------------------------------------
    
    return db_booking
```

---

### 5. Actualización de Infraestructura (Docker Compose)
**Archivo:** `docker-compose.yml` (Actualizado)
Agregamos el servicio `worker` que ejecutará las tareas de Celery.

```yaml

```

---

### Resumen de Logros en la Semana 4:
1.  **Desacoplamiento:** El API ya no se bloquea esperando a que terminen los cálculos de reportes o lógica administrativa.
2.  **Lógica de Dulces:** Implementada automáticamente para pasajeros menores de 12 años mediante workers.
3.  **Estadísticas en Tiempo Real:** Redis ahora mantiene contadores globales de recaudo y popularidad de destinos, listos para ser consumidos por el slice de Reportes.
4.  **Escalabilidad:** Podemos aumentar el número de réplicas del servicio `worker` de forma independiente al API si el volumen de reservas crece.

**Próximo paso (Semana 5):** Implementaremos la Inteligencia Artificial con LangChain, utilizando los datos que ya estamos recolectando en PostgreSQL y Redis para crear un agente de consulta inteligente.