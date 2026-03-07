import logging
import aiohttp
from aiogram import Bot, Dispatcher

from app.database.manager import DatabaseManager
from app.core.config import settings
from app.services.open_meteo import WeatherAPI


logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    logger.info('Starting the bot...')

    db = DatabaseManager(
        dsn=settings.DB_URL,
        min_size=5,
        max_size=10
    )
    await db.connect()

    session = aiohttp.ClientSession()
    logger.info('HTTP Session successfully created')
    weather = WeatherAPI(settings.WEATHER_BASE_URL, session)

    dispatcher['db'] = db
    dispatcher['http_session'] = session
    dispatcher['weather'] = weather



async def on_shutdown(dispatcher: Dispatcher, ) -> None:
    db: DatabaseManager = dispatcher.get('db') #type:ignore
    http_session: aiohttp.ClientSession = dispatcher.get('http_session') #type:ignore
    # Used type:ignore as its said in documentation of aiogram3

    logger.info('Stopping the bot...')

    await db.disconnect()

    if http_session:
        await http_session.close()
        logger.info('HTTP Session closed')