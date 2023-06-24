from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['start']))
async def process_command_start(message: Message):
    await message.answer(text=message.from_user.id)