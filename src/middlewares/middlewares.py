from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.flags import get_flag
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

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
