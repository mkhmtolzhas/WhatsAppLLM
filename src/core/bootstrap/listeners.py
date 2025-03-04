from fastapi import FastAPI
from src.core.cache.client import cache_client


class Listener:
    @staticmethod
    async def startup():
        await cache_client.startup()
    
    @staticmethod
    async def shutdown():
        await cache_client.close()

    @staticmethod
    def init_listeners(app: FastAPI):
        app.add_event_handler("startup", Listener.startup)
        app.add_event_handler("shutdown", Listener.shutdown)