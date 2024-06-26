import redis.asyncio as redis
from app.core.config import settings


redis_client = redis.Redis.from_url(settings.REDIS_URL)


async def check_redis_connection():
    try:
        ping_response = await redis_client.ping()
        print(f"Conectou com sucesso: {ping_response}")
    except redis.ConnectionError:
        print("Falha ao conectar com Redis")
