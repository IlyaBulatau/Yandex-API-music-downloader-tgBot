from aiogram import Router
from aiogram.types import InlineQuery,InlineQueryResultAudio, InlineQueryResultCachedAudio, InlineQueryResultArticle, InputMediaAudio, InputTextMessageContent, InlineQueryResultPhoto
from services.music_api import music_api

router = Router()


@router.inline_query()
async def process_inline(inline:InlineQuery):

    responce = await music_api.get_responce(inline.query)
    if not responce:
        return
    
    result = []
    for resp in responce:
        result.append(InlineQueryResultArticle(
            id=resp['id'],
            url=resp['image'],
            title=resp['title'],
            input_message_content=InputTextMessageContent(message_text='l'),
        ))

    await inline.answer(results=result, is_personal=True)

    