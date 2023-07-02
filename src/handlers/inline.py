from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.fsm.context import FSMContext

from services.music_api import music_api
from fsm.states import MusicState

router = Router()

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

    
