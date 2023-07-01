from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from documents.texts import CALLBACK, BUTTON_TEXT

def create_kb():
    kb = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text=BUTTON_TEXT['search'], switch_inline_query_current_chat=''),
               InlineKeyboardButton(text=BUTTON_TEXT['coins'], callback_data=CALLBACK['coins'])] 

    kb.row(*buttons, width=1)

    return kb.as_markup()

