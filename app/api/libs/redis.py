import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)


async def check_redis_connection():
    try:
        ping_response = await redis_client.ping()
        print(f"Ping successful: {ping_response}")
    except redis.ConnectionError:
        print("Failed to connect to Redis")
