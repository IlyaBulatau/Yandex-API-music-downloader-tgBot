from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from documents.texts import CALLBACK

def create_kb():
    kb = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text='Search music', switch_inline_query_current_chat=''),
               InlineKeyboardButton(text='My coins', callback_data=CALLBACK['coins'])] 

    kb.row(*buttons, width=1)

    return kb.as_markup()


def inline_kb(data):

    kb = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text='Download', callback_data='d')]
    kb.row(*buttons, width=1)

    return kb.as_markup()
