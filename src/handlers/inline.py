from aiogram import Router, Bot
from aiogram.types import InlineQuery,InlineQueryResultAudio, InlineQueryResultArticle, InputTextMessageContent, Message, InputMediaAudio, URLInputFile
from aiogram.methods import AnswerInlineQuery
from aiogram.fsm.context import FSMContext

from services.music_api import music_api
from fsm.states import MusicState
from middlewares.middlewares import LongOperationMiddleware, LimitTrackDownloadInDayMiddleware

router = Router()
router.message.middleware(LimitTrackDownloadInDayMiddleware())
router.message.middleware(LongOperationMiddleware())

@router.inline_query()
async def process_inline(inline: InlineQuery, state: FSMContext):
    """
    Реагирует на упаминания бота в инлайн режиме

    Ищет и отображает треки по введенному тексту

    Устанавливает состояия ожидания получения ИД трека посел клика юзера по треку
    """

    responces = await music_api.get_responce(inline.query)
    if not responces:
        return
    
    result = []

    for responce in responces:
        result.append(
            InlineQueryResultArticle(
            id=str(responce['id']),
            title=responce['title'],
            input_message_content=InputTextMessageContent(message_text='search_music_for_id_'+str(responce['id'])),
            thumb_url=responce['photo'],
            )
        )

    await state.set_state(MusicState.id)

    await inline.answer(results=result, is_personal=True)

    
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
    await state.update_data(id=message.text.split('_')[-1])

    data = await state.get_data()
    id = data.get('id')

    music, title, artist = await music_api.get_music_by_id(id)
    
    await state.clear()
    
    await bot.send_audio(chat_id=message.chat.id, audio=URLInputFile(url=music), performer=artist, title=title, protect_content=True)  
    