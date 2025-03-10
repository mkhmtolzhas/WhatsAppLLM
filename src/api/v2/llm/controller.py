import asyncio
from .service import llm_service
from src.core.messaging.broker import broker
from .schemas import LLMRequest, LLMResponse
from aio_pika import IncomingMessage
import json



class Controller:
    @staticmethod
    async def consuming():
        try:
            await broker.consume(callback=Controller.callback, queue_name="whatsapp", exchange_name="whatsapp", routing_key="whatsapp")
        except Exception as e:
            print(e)

    @staticmethod
    async def callback(message: IncomingMessage):
        async with message.process():
            message = json.loads(message.body.decode())
            print("Received message", message)
            response = await llm_service.get_response(LLMRequest(**message))
            await broker.publish(exchange_name="llm", routing_key="llm", data=response.model_dump())
