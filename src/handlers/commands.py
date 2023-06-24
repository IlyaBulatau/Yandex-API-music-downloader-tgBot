from aiogram import Router
from aiogram.filters import Text, Command
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from aiogram.fsm.context import FSMContext

from documents.texts import COMMANDS, CALLBACK
from middlewares.middlewares import AddNewUserMiddleware
from database.models import User
from keyboards.keyboards import create_kb

router = Router()
router.message.middleware(AddNewUserMiddleware())

@router.message(Command(commands=['start']), flags={'flag_n ew_user': 'flag_new_user'})
async def process_command_start(message: Message, state: FSMContext):
    # получить кэш состояний
    get_state = await state.get_state()
    # если кэш не пустой то очищает его    
    if get_state != None:
        state.clear()

    await message.answer(text=COMMANDS['start'], reply_markup=create_kb())


@router.callback_query(Text(text=CALLBACK['coins']))
async def process_get_coins_by_user_tg_id(callback: CallbackQuery):
    """
    ВДля работы с монетами юзера
    """
    text = await User.get_coins(tg_id=callback.from_user.id)
    await callback.message.answer(text=str(text))

@router.inline_query()
async def process_inline(inline:InlineQuery):
    await inline.answer(results=[
        InlineQueryResultArticle(id=1, title='A', input_message_content=InputTextMessageContent(message_text='A')),
        InlineQueryResultArticle(id=2, title='B', input_message_content=InputTextMessageContent(message_text='B')),
        InlineQueryResultArticle(id=3, title='C', input_message_content=InputTextMessageContent(message_text='C'))
    ], is_personal=True, )