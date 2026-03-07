from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    waiting_for_location = State()