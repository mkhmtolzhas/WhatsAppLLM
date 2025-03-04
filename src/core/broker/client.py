import asyncio
from src.core.cache.client import cache_client, CacheClient
from src.api.v1.llm.schemas import LLMRequest
from json import loads

class BrokerClient:
    def __init__(self, cache_client: CacheClient = cache_client):
        self.client = cache_client.redis
        self.publish_channel = "llm_to_whatsapp"
        self.subscribe_channel = "whatsapp_to_llm"
        self.pubsub = self.client.pubsub()
        self.subtask = None

    async def publish(self, channel: str, message: str):
        await self.client.publish(channel, message)

    async def _listen(self, callback: callable):
        await self.pubsub.subscribe(self.subscribe_channel)

        try:
            while True:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    data = loads(message["data"])
                    print(data)
                    request = LLMRequest(message=data["message"], user=data["user"])
                    response = await callback(request)
                    await self.publish(self.publish_channel, response.model_dump())
                await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Ошибка подписки на Redis: {e}")
        finally:
            await self.pubsub.close()
    
    async def subscribe(self, callback: callable):
        if self.subtask is None:
            self.subtask = asyncio.create_task(self._listen(callback))
        
    async def close(self):
        await self.client.close()

broker_client = BrokerClient(cache_client=cache_client)
