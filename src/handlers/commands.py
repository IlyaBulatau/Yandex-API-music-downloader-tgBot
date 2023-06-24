from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message
from middlewares.middlewares import AddNewUserMiddleware

router = Router()
router.message.middleware(AddNewUserMiddleware())

@router.message(Command(commands=['start']), flags={'flag_new_user': 'flag_new_user'})
async def process_command_start(message: Message):
    await message.answer(text=message.from_user.id)