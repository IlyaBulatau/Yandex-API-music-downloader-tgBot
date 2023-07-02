from documents.texts import CALLBACK
from  database.models import User

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from fsm.states import PaymentState
from keyboards.keyboards import buy_coins_kb
from services.payments.yoomoney_api import payment
from config import config

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
async def start_process_buy_coins(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PaymentState.count)

    await callback.message.answer(text=f'How many coins do you want to buy?\n\nEnter quantity as a positive integer\n\nThe cost of 1 coin is {config.ONE_COIN_QUANTITY}₽')
    await callback.answer()

@router.callback_query(Text(startswith=CALLBACK['payment_ver']))
async def process_verefication_payment(callback: CallbackQuery):
    verificate = payment.is_succssesful_payment(callback.data)
    if verificate.details:
        await callback.message.answer(text='You have successfully bought coins!\n\nCongratulations and thanks!')
    else:
        await callback.message.answer(text='Payment not found\nCoins not purchased')

    await callback.answer()