import json
from src.core.config import settings
from aio_pika import connect_robust, ExchangeType, Message, DeliveryMode


class Broker:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
    
    async def connect(self):
        self.connection = await connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        print("Connected to RabbitMQ")
    
    async def publish(self, exchange_name: str, routing_key: str, data: dict):
        exchange = await self.channel.declare_exchange(exchange_name, ExchangeType.DIRECT)
        message = Message(body=json.dumps(data).encode())
        await exchange.publish(message, routing_key=routing_key)
    
    async def consume(self, callback: callable, queue_name: str, exchange_name: str, routing_key: str):
        exchange = await self.channel.declare_exchange(exchange_name, ExchangeType.DIRECT)
        queue = await self.channel.declare_queue(queue_name)
        await queue.bind(exchange, routing_key)
        await queue.consume(callback)
    
    async def close(self):
        await self.connection.close()


broker = Broker(settings.rabbitmq_url)