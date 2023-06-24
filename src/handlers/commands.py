from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from documents.texts import COMMANDS
from middlewares.middlewares import AddNewUserMiddleware
from database.models import User


router = Router()
router.message.middleware(AddNewUserMiddleware())

@router.message(Command(commands=['start']), flags={'flag_n ew_user': 'flag_new_user'})
async def process_command_start(message: Message, state: FSMContext):
    get_state = await state.get_state()
    if get_state != None:
        state.clear()

    await message.answer(text=COMMANDS['start'])

@router.message(Command(commands=['coins']))
async def process_command_coins(message: Message):
    text = await User.get_coins(tg_id=message.from_user.id)
    await message.answer(text=str(text))