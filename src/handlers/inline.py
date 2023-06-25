from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultAudio


router = Router()


@router.inline_query()
async def process_inline(inline:InlineQuery):
    await inline.answer(results=[
        InlineQueryResultArticle(id=1, title='A', input_message_content=InputTextMessageContent(message_text='A')),
        InlineQueryResultArticle(id=2, title='B', input_message_content=InputTextMessageContent(message_text='B')),
        InlineQueryResultArticle(id=3, title='C', input_message_content=InputTextMessageContent(message_text='C'))
    ], is_personal=True)