# Runbook de Operaciones - Flight Reservation System

Guía operativa para el equipo de infraestructura y desarrollo.

---

## 1. Reinicio de Servicios

### API Server
```bash
# Docker Compose
docker compose restart api

# Kubernetes
kubectl rollout restart deployment/flight-api -n flight-system
kubectl rollout status deployment/flight-api -n flight-system
```

### Celery Worker
```bash
# Docker Compose
docker compose restart worker

# Kubernetes
kubectl rollout restart deployment/flight-worker -n flight-system
```

### Base de Datos (PostgreSQL)
```bash
# Docker Compose (precaución: desconecta clientes activos)
docker compose restart db

# Verificar conexiones activas antes de reiniciar
docker compose exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

### Redis
```bash
# Docker Compose
docker compose restart redis

# Verificar uso de memoria antes de reiniciar
docker compose exec redis redis-cli info memory | grep used_memory_human
```

### RabbitMQ
```bash
# Docker Compose
docker compose restart rabbitmq

# Verificar colas pendientes antes de reiniciar
docker compose exec rabbitmq rabbitmqctl list_queues name messages
```

---

## 2. Problemas Comunes y Soluciones

### 2.1 Error de conexión a PostgreSQL

**Síntoma:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Diagnóstico:**
```bash
# Verificar que el contenedor está corriendo
docker compose ps db

# Verificar logs
docker compose logs db --tail=50

# Probar conexión manual
docker compose exec db psql -U postgres -c "SELECT 1;"
```

**Solución:**
1. Si el contenedor no está corriendo: `docker compose up -d db`
2. Si hay demasiadas conexiones: verificar pool de SQLAlchemy (`pool_size`, `max_overflow`)
3. Si el disco está lleno: liberar espacio o expandir volumen
4. Verificar `DATABASE_URL` en variables de entorno

### 2.2 Redis sin memoria

**Síntoma:** `OOM command not allowed when used memory > maxmemory`

**Diagnóstico:**
```bash
docker compose exec redis redis-cli info memory
docker compose exec redis redis-cli dbsize
```

**Solución:**
1. Verificar keys acumuladas: `docker compose exec redis redis-cli --scan --pattern '*' | head -20`
2. Limpiar keys expiradas: `docker compose exec redis redis-cli FLUSHDB` (solo en desarrollo)
3. En producción: aumentar `maxmemory` o configurar política de evicción `allkeys-lru`
4. Revisar si hay keys sin TTL que deberían tenerlo

### 2.3 Tareas Celery atascadas

**Síntoma:** tareas en estado PENDING indefinidamente o workers no procesan.

**Diagnóstico:**
```bash
# Verificar workers activos
docker compose exec worker celery -A src.worker.celery_app inspect active

# Verificar colas
docker compose exec rabbitmq rabbitmqctl list_queues name messages consumers

# Ver tareas reservadas
docker compose exec worker celery -A src.worker.celery_app inspect reserved
```

**Solución:**
1. Si no hay workers: reiniciar el servicio worker
2. Si hay mensajes sin consumidores: verificar que el worker se conecta al broker correcto
3. Purgar cola atascada (último recurso): `celery -A src.worker.celery_app purge`
4. Verificar `RABBITMQ_URL` en variables de entorno del worker

### 2.4 Error de Groq API (agente IA)

**Síntoma:** `groq.APIError` o timeout en endpoints `/api/v1/ai/`

**Diagnóstico:**
```bash
# Verificar que la API key está configurada
docker compose exec api env | grep GROQ_API_KEY

# Probar conectividad
docker compose exec api curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY" | head -5
```

**Solución:**
1. Si no hay API key: configurar `GROQ_API_KEY` en `.env`
2. Si hay rate limiting: implementar backoff o reducir frecuencia de requests
3. Si hay timeout: verificar conectividad de red del contenedor
4. Los endpoints REST siguen funcionando sin Groq; solo IA se ve afectada

---

## 3. Monitoreo y Alertas (Prometheus/Grafana)

### Métricas clave a monitorear

| Métrica | Umbral de alerta | Acción |
|---------|-------------------|--------|
| `http_request_duration_seconds` P95 | > 2s | Investigar queries lentas |
| `http_requests_total` (5xx) | > 5/min | Revisar logs de errores |
| `celery_tasks_failed_total` | > 10/hora | Revisar logs del worker |
| `pg_stat_activity_count` | > 80% max_connections | Revisar pool de conexiones |
| `redis_used_memory_bytes` | > 80% maxmemory | Limpiar keys o escalar |
| `rabbitmq_queue_messages` | > 1000 | Escalar workers |

### Dashboards Grafana recomendados

1. **API Overview**: latencia P50/P95/P99, throughput, tasa de errores
2. **Database**: conexiones activas, queries/s, tamaño de tablas
3. **Redis**: hit rate, memoria, keys por patrón
4. **Celery**: tareas/min, duración promedio, tasa de fallos
5. **Infrastructure**: CPU, memoria, disco, red por pod

### Configurar alertas
```yaml
# Ejemplo de regla Prometheus
groups:
  - name: flight-system
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Tasa alta de errores 5xx en API"
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Latencia P95 superior a 2 segundos"
```

---

## 4. Escalamiento

### Horizontal Pod Autoscaler (HPA)

```bash
# Ver estado actual del HPA
kubectl get hpa -n flight-system

# Escalar manualmente la API
kubectl scale deployment/flight-api --replicas=4 -n flight-system

# Escalar workers Celery
kubectl scale deployment/flight-worker --replicas=3 -n flight-system
```

**Configuración HPA recomendada:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flight-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flight-api
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

### Escalamiento de nodos

```bash
# AWS EKS - verificar nodos
kubectl get nodes

# Escalar node group (Terraform o eksctl)
eksctl scale nodegroup --cluster=flight-cluster --name=workers --nodes=5

# Verificar pods pendientes por falta de recursos
kubectl get pods -n flight-system --field-selector=status.phase=Pending
```

---

## 5. Backup y Recuperación

### PostgreSQL (RDS Snapshots)

```bash
# Crear snapshot manual (AWS CLI)
aws rds create-db-snapshot \
  --db-instance-identifier flight-db \
  --db-snapshot-identifier flight-db-backup-$(date +%Y%m%d)

# Listar snapshots existentes
aws rds describe-db-snapshots \
  --db-instance-identifier flight-db \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,SnapshotCreateTime,Status]' \
  --output table

# Restaurar desde snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier flight-db-restored \
  --db-snapshot-identifier flight-db-backup-20250301
```

### Backup manual con pg_dump (Docker)

```bash
# Crear backup
docker compose exec db pg_dump -U postgres flight_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker compose exec -T db psql -U postgres flight_db < backup_20250301.sql
```

### Redis (persistencia)

Redis se usa como caché y contadores. En caso de pérdida:
- Los contadores se recalculan automáticamente desde PostgreSQL
- No se requiere backup de Redis en este sistema

---

## 6. Checklist de Respuesta a Incidentes

### Severidad 1 - Sistema caído
- [ ] Verificar estado de todos los servicios: `docker compose ps` / `kubectl get pods`
- [ ] Revisar logs del servicio afectado: `docker compose logs <servicio> --tail=100`
- [ ] Verificar conectividad de red entre servicios
- [ ] Verificar variables de entorno y secrets
- [ ] Si es DB: verificar disco, conexiones, locks
- [ ] Reiniciar servicio afectado y monitorear recuperación
- [ ] Notificar al equipo en canal de incidentes
- [ ] Documentar timeline y root cause post-incidente

### Severidad 2 - Degradación de rendimiento
- [ ] Revisar métricas en Grafana (latencia, error rate)
- [ ] Identificar servicio con problemas (API, DB, Redis, Worker)
- [ ] Verificar si hubo despliegue reciente (posible rollback)
- [ ] Revisar queries lentas: `pg_stat_statements` o logs slow query
- [ ] Verificar tamaño de colas en RabbitMQ
- [ ] Escalar horizontalmente si es necesario
- [ ] Monitorear durante 30 minutos post-mitigación

### Severidad 3 - Funcionalidad parcial afectada
- [ ] Identificar feature afectada (vuelos, reservas, IA, stats)
- [ ] Revisar logs específicos del feature
- [ ] Verificar dependencias externas (Groq API, si es IA)
- [ ] Crear ticket con reproducción del problema
- [ ] Aplicar fix en siguiente ventana de despliegue
