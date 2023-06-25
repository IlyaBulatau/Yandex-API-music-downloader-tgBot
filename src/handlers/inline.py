from aiogram import Router
from aiogram.types import InlineQuery,InlineQueryResultAudio, InlineQueryResultArticle, InputMediaAudio, InputTextMessageContent, InlineQueryResultPhoto, InputMessageContent
from services.music_api import music_api
from keyboards.keyboards import inline_kb

router = Router()


@router.inline_query()
async def process_inline(inline:InlineQuery):

    responces = await music_api.get_responce(inline.query)
    if not responces:
        return
    
    result = []

    for responce in responces:
        result.append(InlineQueryResultAudio(
            type='audio',
            id=responce['id'],
            title=responce['title']+', '+responce['artist'],
            audio_url=responce['audio'],
            audio_duration=responce['duration'],
            reply_markup=inline_kb(responce),
            input_message_content=InputTextMessageContent(message_text='Download')
        ))


    await inline.answer(results=result, is_personal=True)

    
