from aiogram.types import Message, URLInputFile
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from middlewares.middlewares import LongOperationMiddleware, LimitTrackDownloadInDayMiddleware

from fsm.states import MusicState, PaymentState
from services.music_api import music_api
from documents.texts import CALLBACK
from services.payments.yoomoney_api import payment
from keyboards.keyboards import create_payment_accept_kb
from config import config
from datetime import datetime

router = Router()
router.message.middleware(LimitTrackDownloadInDayMiddleware())
router.message.middleware(LongOperationMiddleware())

@router.message(lambda msg: msg.text.startswith('search_music_for_id_') and len(msg.text.split('_')[-1]) >= 8 and msg.text.split('_')[-1].isdigit(), # лямбда для более точнго определения
                # что юзер именно выбрал трек а не просто ввел текст сообщением, так как клик по треку в инлайн режиме возвращает апдейт сообщение 
                MusicState.id, 
                flags={'limit_download': 'limit_download', 'upload_document': 'upload_document'})
async def process_download_misuc(message: Message, state: FSMContext, bot: Bot):
    """
    Отрабатывает после того как юзер выбрал трек
    Удаляет сообщение с номером трека и запоминает ИД трека

    Ищет трек по ИД и отдает результат для скачивания
    """

    await message.delete()

    await message.answer(text='⌛ Wait for the file to load')

    await state.update_data(id=message.text.split('_')[-1])

    data = await state.get_data()
    id = data.get('id')

    music, title, artist = await music_api.get_music_by_id(id)
    
    await state.clear()
    
    await bot.send_audio(chat_id=message.chat.id, audio=URLInputFile(url=music, filename=title+'.wav'), performer=artist, title=title)  
    

@router.message(lambda msg: isinstance(msg.text, (int, str)) and str(msg.text).isdigit() and int(msg.text) > 0, PaymentState.count)
async def process_get_count_coins_for_payment(message: Message, state: FSMContext):
    
    await state.update_data(count=message.text)
    data = await state.get_data()
    quantity = int(data['count']) * int(config.ONE_COIN_QUANTITY)
    await state.clear()

    label = CALLBACK['payment_ver']+str(message.from_user.id)+str(datetime.now().strftime('%Y:%m:%d:%H:%M:%S'))
    payment_url = payment.get_payments_url(quantity, label)
    await message.answer(text=payment_url, reply_markup=create_payment_accept_kb(label))

@router.message(PaymentState.count)
async def process_not_valid_count_value(message: Message):
    await message.answer(text='✖ You entered the number incorrectly\n\nTry again\n\n↪️ To exit the purchase state /start')
