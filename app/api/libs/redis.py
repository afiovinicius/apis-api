import redis.asyncio as redis
from app.core.config import settings

REDIS_URL = settings.REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL)
print(f"REDIS_URL from environment: {settings.REDIS_URL, REDIS_URL} ")


async def check_redis_connection():
    try:
        ping_response = await redis_client.ping()
        print(f"Ping successful: {ping_response}")
    except redis.ConnectionError:
        print("Failed to connect to Redis")
