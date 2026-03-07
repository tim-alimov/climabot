from aiohttp import ClientSession
from contextlib import suppress

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.database.regions import UZB_REGIONS, UZB_REGIONS_COORDS
from app.database.manager import DatabaseManager

from app.keyboards.reply_buttons import location_methods_menu, main_menu
from app.keyboards.inline_buttons import regions_buttons

from app.core.exceptions import DatabaseError, GeocodeFetchingError
from app.states.user_states import BotState
from app.services.geocoding import get_region_name




locations_router = Router()

@locations_router.message(F.text == "🗺 Choose Region", BotState.waiting_for_location)
async def on_regions(message: Message) -> None:
    assert message.bot is not None

    await message.answer(
        text='📍 Please select your region below:',
        reply_markup=regions_buttons(regions=UZB_REGIONS)
    )


@locations_router.callback_query(F.data == 'back', BotState.waiting_for_location)
async def on_back(call: CallbackQuery) -> None:
    assert call.message is not None and call.message.bot is not None and call.bot is not None

    await call.answer()

    with suppress(TelegramBadRequest):
        await call.bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

    await call.message.answer(
        text='Please share your location or choose a region to continue.',
        reply_markup=location_methods_menu()
    )


@locations_router.message(F.location, BotState.waiting_for_location)
async def on_location(message: Message, state: FSMContext, db: DatabaseManager, http_session: ClientSession) -> None:
    assert message.location is not None and message.bot is not None and message.from_user is not None

    latitude = message.location.latitude
    longitude = message.location.longitude


    try:
        region = await get_region_name(session=http_session, lat=latitude, lng=longitude)

        await db.insert_location(
            user_id=message.from_user.id,
            region_name=region,
            lat=latitude,
            lng=longitude
        )

        await message.answer(
            text= f"📍 Location set  to <b>{region}</b>.\nYou can now use the buttons below to get weather information\n\n<b>Note</b>: You can change your location anytime using Change location.",
            reply_markup= main_menu
        )

        await state.clear()

    except DatabaseError:
        await message.answer(
            text='Server side error occurred. Please, try after a while. We are working on it.',
            reply_markup=location_methods_menu()
        )

    except GeocodeFetchingError:
        await message.answer(
            text="Server side error occurred. Please, choose a region manually or try after a while. We are working on it.", 
            reply_markup=location_methods_menu()
        )


@locations_router.callback_query(F.data.startswith('reg:'), BotState.waiting_for_location)
async def on_region_callback(call: CallbackQuery, state: FSMContext, db: DatabaseManager) -> None:
    assert call.data is not None and call.message is not None and call.message.bot is not None and call.bot is  not None

    await call.answer()

    try:
        region = call.data.removeprefix('reg:')
        location = UZB_REGIONS_COORDS[region]
        latitude = location['lat']
        longitude = location['lng']

        await db.insert_location(
            user_id=call.from_user.id,
            region_name=region,
            lat=latitude,
            lng = longitude
        )

        with suppress(TelegramBadRequest):
            await call.bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )

        await call.message.answer(
            text= f"📍 Location set  to <b>{region}</b>.\nYou can now use the buttons below to get weather information\n\n<b>Note</b>: You can change your location anytime using Change location.",
            reply_markup= main_menu
        )

        await state.clear()


    except KeyError:
        await call.message.answer(
            text="Server side error occurred. Region selection method is currently not available. Please, send your location.", reply_markup=location_methods_menu()
        )
    
    except DatabaseError:
        await call.message.answer(
            text="Server side error occurred. Please, try after a while. We are working on it.",
            reply_markup=location_methods_menu())



@locations_router.message(F.text == '🗺️ Change location')
async def on_change_location(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Choose a method to set your location", 
        reply_markup=location_methods_menu(back_button=True)
    )

    await state.set_state(BotState.waiting_for_location)


@locations_router.message(F.text == '⬅️ Back', BotState.waiting_for_location)
async def on_location_back(message: Message, state: FSMContext)-> None:
    await message.answer(
        text="You are back to main menu", 
        reply_markup=main_menu
    )

    await state.clear()