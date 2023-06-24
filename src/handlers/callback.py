from documents.texts import CALLBACK
from  database.models import User

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(Text(text=CALLBACK['coins']))
async def process_get_coins_by_user_tg_id(callback: CallbackQuery):
    """
    Для работы с монетами юзера
    """
    text = await User.get_coins(tg_id=callback.from_user.id)
    await callback.message.answer(text=str(text))
    await callback.answer()
