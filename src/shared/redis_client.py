import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def update_stat(key: str, amount: float):
    """Incrementa un valor en Redis (útil para recaudos y contadores)."""
    redis_client.incrbyfloat(key, amount)


def log_to_list(key: str, value: str):
    """Agrega un evento a una lista en Redis (útil para logs de dulces)."""
    redis_client.lpush(key, value)