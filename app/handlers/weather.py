from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from app.database.manager import DatabaseManager
from app.keyboards.reply_buttons import location_methods_menu

from app.states.user_states import BotState
from app.core.exceptions import DatabaseError, OpenMeteoFetchingError
from app.services.open_meteo import WeatherAPI


weather_router = Router()


@weather_router.message(F.text == 'Today')
async def on_today(message: Message, db: DatabaseManager, weather: WeatherAPI, state: FSMContext) -> None:
    assert message.from_user is not None and message.bot is not None
    user_id = message.from_user.id

    try:
        location = await db.get_location(user_id)

        if not location:
            await message.answer(
                text="Please, send your location first", 
                reply_markup=location_methods_menu()
            )

            await state.set_state(BotState.waiting_for_location)
            return

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            response = await weather.get_current_weather(location.lat, location.lng)

            await message.answer(
                text=response.formatted_message, 

            )

    except (DatabaseError, OpenMeteoFetchingError):
        await message.answer(
            text='Server side error. Please, try after a while. We are working on it.'
        )


@weather_router.message(F.text == 'Forecast')
async def on_forecast(message: Message, db: DatabaseManager, weather: WeatherAPI, state: FSMContext) -> None:
    assert message.from_user is not None and message.bot is not None
    user_id = message.from_user.id

    try:
        location = await db.get_location(user_id)

        if not location:
            await message.answer(
                text="Please, send your location first", 
                reply_markup=location_methods_menu()
            )

            await state.set_state(BotState.waiting_for_location)
            return

        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            response = await weather.get_forecast(location.lat, location.lng)

            await message.answer(
                text=response.formatted_message,
            )

    except (DatabaseError, OpenMeteoFetchingError):
        await message.answer(
            text='Server side error. Please, try after a while. We are working on it.'
        )