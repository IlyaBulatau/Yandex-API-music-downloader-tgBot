from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.flags import get_flag
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from database.models import User


class AddNewUserMiddleware(BaseMiddleware):
    """
    Отслеживает добавление нового юзера
    """

    async def __call__(sellf,
                handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                event: Message | CallbackQuery,
                data: Dict[str, Any]):
        
        # утсановка флага для метки на хендлерах
        track_new_user_flag = get_flag(handler=data, name='flag_new_user')

        # если хендлер помечен флагом
        if track_new_user_flag:
            # добавляет юзера в базу данных   
            await User(tg_id=event.from_user.id, username=event.from_user.username).save()
        
        return await handler(event, data)


class LongOperationMiddleware(BaseMiddleware):
    """
    Обозначает проложительные хендлеры что бы юзер знал что бот не отключился а выполняет операцию
    """

    async def __call__(sellf,
                handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                event: Message | CallbackQuery,
                data: Dict[str, Any]):
        
        flag = get_flag(handler=data ,name='upload_document')

        if flag:
            async with ChatActionSender(chat_id=event.chat.id, action=flag):
                return await handler(event, data) 


        return await handler(event, data)
