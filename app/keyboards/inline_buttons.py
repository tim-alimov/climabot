from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def regions_buttons(regions: list|tuple) -> InlineKeyboardMarkup:
    buttons  = InlineKeyboardBuilder()

    for region in regions:
        buttons.add(InlineKeyboardButton(text=region, callback_data= f'reg:{region}'))

    buttons.add(InlineKeyboardButton(text='Back ⬅️', callback_data='back', style='danger'))
    buttons.adjust(2)

    return buttons.as_markup()