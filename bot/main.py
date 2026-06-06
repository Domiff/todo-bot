import asyncio
import logging

from aiogram_dialog import setup_dialogs

from bot.auth import register_router
from bot.core.setup import create_bot, create_dispatcher
from bot.todo import todo_router


async def main():
    bot = create_bot()
    dp = create_dispatcher()

    dp.include_router(register_router)
    dp.include_router(todo_router)

    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
