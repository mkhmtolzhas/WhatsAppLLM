from fastapi import FastAPI
from src.core.cache.client import cache_client
from src.core.broker.client import broker_client
from src.api.v1.llm.service import llm_service


class Listener:
    @staticmethod
    async def startup():
        await cache_client.startup()
        # await broker_client.subscribe(llm_service.get_response)
    
    @staticmethod
    async def shutdown():
        # await broker_client.close()
        await cache_client.close()

    @staticmethod
    def init_listeners(app: FastAPI):
        app.add_event_handler("startup", Listener.startup)
        app.add_event_handler("shutdown", Listener.shutdown)