from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from documents.texts import COMMANDS
from middlewares.middlewares import AddNewUserMiddleware
from keyboards.keyboards import create_kb
from services.music_api import music_api


router = Router()
router.message.middleware(AddNewUserMiddleware())

@router.message(Command(commands=['start']), flags={'flag_n ew_user': 'flag_new_user'})
async def process_command_start(message: Message, state: FSMContext):
    # получить кэш состояний
    get_state = await state.get_state()
    # если кэш не пустой то очищает его    
    if get_state != None:
        state.clear()

    await message.answer(text=COMMANDS['start'], reply_markup=create_kb())

