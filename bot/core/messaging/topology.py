from aio_pika.abc import AbstractChannel, ExchangeType

TASKS_EXCHANGE = "todo.tasks"

EXCHANGES = {
    TASKS_EXCHANGE: ExchangeType.DIRECT,
}

TASKS_CREATED_ROUTING_KEY = "tasks.created"
TASK_CREATED_QUEUE = "todo-bot.tasks.created"
QUEUES = {
    TASK_CREATED_QUEUE: (TASKS_EXCHANGE, TASKS_CREATED_ROUTING_KEY)
}


async def declare_exchanges(channel: AbstractChannel) -> None:
    for name, exchange_type in EXCHANGES.items():
        await channel.declare_exchange(
            name=name,
            type=exchange_type,
            durable=True
        )


async def declare_queues(channel: AbstractChannel) -> None:
    for queue_name, (exchange_name, routing_key) in QUEUES.items():
        queue = await channel.declare_queue(name=queue_name, durable=True)
        await queue.bind(exchange=exchange_name, routing_key=routing_key)
