from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.states.user_states import BotState
from app.keyboards.reply_buttons import location_methods_menu, main_menu
from app.database.manager import DatabaseManager, DatabaseError



starter_router = Router()


@starter_router.message(CommandStart())
async def on_start(message: Message, state: FSMContext, db: DatabaseManager) -> None:
    assert message.from_user is not None

    user_id = message.from_user.id

    try:

        location = await db.get_location(user_id)

        if not location:
            await message.answer(
                text='Hi! 🌤 To get the current forecast, please share your location or choose a region below.',
                reply_markup=location_methods_menu()
            )
            await state.set_state(BotState.waiting_for_location)
            return

        await message.answer(
            text=f'Your location is already set to <b>{location.region_name}</b>.\n\n<b>Note:</b> To update it, choose Change location.',
            reply_markup=main_menu
        )

        await state.clear()

    except DatabaseError:
        await message.answer(
            text="Server side error occurred. Please, try after a while. We are working on it."
        )
        