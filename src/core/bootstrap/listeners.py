from fastapi import FastAPI
from src.core.cache.client import cache_client
from src.core.messaging.broker import broker
from src.api.v2.llm.controller import Controller
from asyncio import create_task

class Listener:
    @staticmethod
    async def startup():
        await cache_client.startup()
        await broker.connect()
        await Controller.consuming()
    
    @staticmethod
    async def shutdown():
        await cache_client.close()
        await broker.close()

    @staticmethod
    def init_listeners(app: FastAPI):
        app.add_event_handler("startup", Listener.startup)
        app.add_event_handler("shutdown", Listener.shutdown)