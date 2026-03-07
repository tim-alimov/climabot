from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def location_methods_menu(back_button:bool = False):
    buttons = ReplyKeyboardBuilder()
    buttons.add(KeyboardButton(text= '🗺 Choose Region')) 
    buttons.add(KeyboardButton(text= '📍 Share Location', request_location=True))

    if back_button:
        buttons.add(KeyboardButton(text='⬅️ Back'))

    buttons.adjust(2)
    return buttons.as_markup(resize_keyboard=True, input_field_placeholder='Choose...')


main_menu =  ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text='Today'), KeyboardButton(text='Forecast')],
        [KeyboardButton(text='🗺️ Change location')]
    ],
    resize_keyboard=True,
    input_field_placeholder= 'Menu...'
)