# Skill: Docker Operations

Manage Docker services for the Flight Reservation System.

## Instructions

Based on what the user asks, execute the appropriate docker operation:

### Start all services
```bash
docker compose up --build -d
```

### Check status
```bash
docker compose ps
```

### View logs
```bash
# All services
docker compose logs -f --tail 50

# Specific service (api, worker, db, redis, rabbitmq)
docker compose logs -f {service} --tail 50
```

### Restart a service
```bash
docker compose restart {service}
```

### Full reset (destroys data)
Confirm with the user before running this:
```bash
docker compose down -v && docker compose up --build -d
```

### Rebuild only API
```bash
docker compose up --build api -d
```

### Access service shells
```bash
# Redis CLI
docker compose exec redis redis-cli

# PostgreSQL
docker compose exec db psql -U user -d flights

# API shell
docker compose exec api bash
```

### Check Redis stats
```bash
docker compose exec redis redis-cli GET stats:total_revenue
docker compose exec redis redis-cli GET stats:total_infant_count
docker compose exec redis redis-cli GET stats:total_candy_cost
docker compose exec redis redis-cli GET stats:total_pet_bookings
docker compose exec redis redis-cli LRANGE logs:candy_distribution 0 -1
```

### Check RabbitMQ
- Management UI: http://localhost:15672 (admin / admin123)

### Services and ports
| Service  | Port  |
|----------|-------|
| api      | 8000  |
| db       | 5432  |
| redis    | 6379  |
| rabbitmq | 5672, 15672 |
