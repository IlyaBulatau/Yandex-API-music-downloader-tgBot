from documents.texts import CALLBACK
from  database.models import User

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from keyboards.keyboards import buy_coins_kb
from services.payments.yoomoney_api import payment

router = Router()

@router.callback_query(Text(text=CALLBACK['coins']))
async def process_get_coins_by_user_tg_id(callback: CallbackQuery):
    """
    Для работы с монетами юзера
    """
    coins = await User.get_coins(tg_id=callback.from_user.id)
    await callback.message.answer(text=f'You have {coins} coins', reply_markup=buy_coins_kb())
    await callback.answer()

@router.callback_query(Text(text=CALLBACK['buy_coins']))
async def process_answer_url_for_buy_coins(callback: CallbackQuery):
    payment_url = payment.get_payments_url(100, '100')
    await callback.message.answer(text=payment_url)