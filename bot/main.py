import asyncio
from aiogram import Bot, Dispatcher
from handlers.callback_handlers import callback_router
from handlers.command_handlers import command_router
from handlers.vacancy_handlers import vacancy_router
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher()
dispatcher.include_router(callback_router)
dispatcher.include_router(command_router)
dispatcher.include_router(vacancy_router)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
