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
from logger.logger import logger

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
    """
    Запрашивает ввести число монет для покупки
    """
    await state.set_state(PaymentState.count)

    await callback.message.answer(text=f'How many coins do you want to buy?\n\nEnter quantity as a positive integer\n\nThe cost of 1 coin is {config.ONE_COIN_QUANTITY}₽')
    await callback.answer()

@router.callback_query(Text(startswith=CALLBACK['payment_ver']))
async def process_verefication_payment(callback: CallbackQuery):
    """
    Проверяет оплату
    """
    verificate = payment.is_succssesful_payment(callback.data) # если оплата есть вернет сумму если нет False
    if verificate:
        user_coins = await User.get_coins(callback.from_user.id) # монеты юзера
        coins_buy = verificate//config.ONE_COIN_QUANTITY # монеты купленные
        coins = int(user_coins)+int(coins_buy) # всего монет для юзера
        await User.update_coins(tg_id=callback.from_user.id, coins=coins)
        await callback.message.answer(text='You have successfully bought coins!\n\nCongratulations and thanks!')
        logger.critical(f'USER WITH ID {callback.from_user.id} BUY {coins} COINS')
    else:
        await callback.message.answer(text='Payment not found\nCoins not purchased')

    await callback.answer()