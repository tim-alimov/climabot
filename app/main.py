import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.handlers import starter_router, locations_router, weather_router
from app.utils.consoles import logging_initialize
from app.core.config import settings
from app.core.events import on_startup, on_shutdown


logging_initialize(settings.DEBUG_MODE)


async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default= DefaultBotProperties(parse_mode="HTML")
    )
    
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(starter_router, locations_router, weather_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())