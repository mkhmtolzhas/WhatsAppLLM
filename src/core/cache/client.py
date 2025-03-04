from redis.asyncio import Redis
from src.core.config import settings

class CacheClient:
    def __init__(self, host: str, port: int):
        self.client = Redis(host=host, port=port, decode_responses=True)

    async def close(self):
        await self.client.aclose()

    async def get(self, key: str):
        return await self.client.get(key)
    
    async def set(self, key: str, value: str, expire: int = 86400):
        await self.client.set(key, value, ex=expire)
    
    async def delete(self, key: str):
        await self.client.delete(key)

cache_client = CacheClient(settings.redis_host, settings.redis_port)

    

    
