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
    # получить кэш состояний
    get_state = await state.get_state()
    # если кэш не пустой то очищает его    
    if get_state != None:
        state.clear()

    await message.answer(text=COMMANDS['start'])

@router.message(Command(commands=['coins']))
async def process_command_coins(message: Message):
    """
    Для работы с монетами пользователя
    """
    text = await User.get_coins(tg_id=message.from_user.id)
    await message.answer(text=str(text))