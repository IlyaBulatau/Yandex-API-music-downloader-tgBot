from aiogram import Router
from aiogram.types import InlineQuery,InlineQueryResultAudio, InlineQueryResultArticle, InputMediaAudio, InputTextMessageContent, InlineQueryResultPhoto, InputMessageContent
from services.music_api import music_api
from keyboards.keyboards import inline_kb

router = Router()


@router.inline_query()
async def process_inline(inline:InlineQuery):

    responce = await music_api.get_responce(inline.query)
    if not responce:
        return
    
    result = []

    # for resp in responce:
    #     result.append(InlineQueryResultArticle(
    #         id=resp['id'],
    #         reply_markup=inline_kb(resp),
    #         title=resp['title'],
    #         input_message_content=InputTextMessageContent(message_text='l'),
    #     ))

    result.append(InlineQueryResultAudio(
        type='audio',
        id=responce['id'],
        audio_url=responce['audio'],
        title='Title',
        audio_duration=responce['duration'],
        reply_markup=inline_kb(responce),
        input_message_content=InputTextMessageContent(message_text='Download')
    ))


    await inline.answer(results=result, is_personal=True)

    
