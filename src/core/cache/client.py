from redis.asyncio import Redis
from src.core.config import settings

class CacheClient:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(url=redis_url, decode_responses=True)

    async def startup(self):
        try:
            await self.redis.ping()
            print("Connected to Redis")
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
    
    async def close(self):
        await self.redis.aclose()

    async def get(self, key: str):
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str, expire: int = 86400):
        await self.redis.set(key, value, ex=expire)
    
    async def delete(self, key: str):
        await self.redis.delete(key)



cache_client = CacheClient(settings.redis_url)

    

    
