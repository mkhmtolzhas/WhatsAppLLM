from redis.asyncio import Redis
from src.core.config import settings

class CacheClient:
    def __init__(self, host: str, port: int, password: str, username: str):
        self.redis = Redis(host=host, port=port, password=password, username=username, decode_responses=True)

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



cache_client = CacheClient(settings.redis_host, settings.redis_port, settings.redis_password, settings.redis_username)

    

    
