import asyncio

from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import setup_dialogs

from bot.auth import TokenExpired, register_router, token_expired
from bot.core.logging import setup_logging
from bot.core.messaging.topology import TASK_QUEUE
from bot.core.setup import create_bot, create_dispatcher
from bot.todo import todo_router
from bot.todo.consumers import consume
from bot.todo.handlers import make_task_events_handler


async def main():
    bot = create_bot()
    dp = create_dispatcher()

    dp.include_router(register_router)
    dp.include_router(todo_router)
    dp.errors.register(token_expired, ExceptionTypeFilter(TokenExpired))

    setup_dialogs(dp)
    task_events_handler = make_task_events_handler(bot)
    consumer = asyncio.create_task(consume(task_events_handler, TASK_QUEUE))
    try:
        await dp.start_polling(bot)
    finally:
        consumer.cancel()
        await asyncio.gather(consumer, return_exceptions=True)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(main())
