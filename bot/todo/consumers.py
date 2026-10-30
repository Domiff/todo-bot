from collections.abc import Awaitable, Callable

from bot.core.logging import get_logger
from bot.core.messaging.connection import get_channel

Handler = Callable[[bytes], Awaitable[None]]
logger = get_logger(name=__name__)


async def consume(hanlder: Handler, queue_name: str):
    channel = await get_channel()
    queue = await channel.get_queue(name=queue_name, ensure=False)
    await channel.set_qos(prefetch_count=10)

    async with queue.iterator() as iterator:
        async for message in iterator:
            try:
                async with message.process():
                    await hanlder(message.body)
            except Exception:
                logger.exception(
                    "Failed to handle message",
                    extra={
                        "message_id": message.message_id,
                        "routing_key": message.routing_key,
                    },
                )
