import redis.asyncio as redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    db=0,
)


async def check_redis_connection():
    try:
        ping_response = await redis_client.ping()
        print(f"Ping successful: {ping_response}")
    except redis.ConnectionError:
        print("Failed to connect to Redis")
