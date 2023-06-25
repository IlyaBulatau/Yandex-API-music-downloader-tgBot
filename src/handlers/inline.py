from aiogram import Router
from aiogram.types import InlineQuery,InlineQueryResultAudio, InlineQueryResultArticle, InputTextMessageContent, Message
from aiogram.methods import AnswerInlineQuery
from aiogram.fsm.context import FSMContext

from services.music_api import music_api
from keyboards.keyboards import inline_kb
from fsm.states import MusicState

router = Router()

@router.inline_query()
async def process_inline(inline: InlineQuery, state: FSMContext):

    responces = await music_api.get_responce(inline.query)
    if not responces:
        return
    
    result = []

    for responce in responces:
        # result.append(InlineQueryResultAudio(
        #     type='audio',
        #     id=responce['id'],
        #     title=responce['title']+', '+responce['artist'],
        #     audio_url=responce['audio'],
        #     audio_duration=responce['duration'],
        #     reply_markup=inline_kb(responce),
        #     input_message_content=InputTextMessageContent(message_text='Download')
        # ))

        result.append(
            InlineQueryResultArticle(
            id=str(responce['id']),
            title=responce['title'],
            input_message_content=InputTextMessageContent(message_text=responce['id']),
            thumb_url=responce['photo'],
            )
        )

    await state.set_state(MusicState.id)

    await inline.answer(results=result, is_personal=True)

    
@router.message(MusicState.id)
async def test(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(id=message.text)

    data = await state.get_data()
    id = data.get('id')

    await state.clear()
    await message.answer(text=id)