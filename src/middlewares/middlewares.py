from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.flags import get_flag
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from database.models import User
from fsm.cache import downloader
from config import config


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


class LimitTrackDownloadInDayMiddleware(BaseMiddleware):
        """
        Ограничивает скачивания на 1 трек в день

        Если user_id == админ то пропускает хендлер
        Если у юзера закончились скачивания  и нету монет то отправляет сообщение о том через сколько времени можно вернуться
        Если закончились скачивания но есть монеты снимает 1 монету и скачивает трек

        При первом скачивании в день выводит уведомление о том что после скачивания заканчивается лимит и последующее скачивания на сегодня будет взывать монеты если они есть
        """

        async def __call__(sellf,
                handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                event: Message | CallbackQuery,
                data: Dict[str, Any]):

            user_id = event.from_user.id 

            flag = get_flag(handler=data, name='limit_download')


            if flag:

                if int(user_id) == int(config.ADMIN_ID):
                    return await handler(event, data)

                count_user_coins = await User.get_coins(user_id)
                is_limit = await downloader.is_a_user_limit(user_id) 
                if is_limit:
                    

                    if count_user_coins == 0:
                        # подсчет времени оставшегося до конца лимита на скачивания
                        ttl_seconds = await downloader.get_user_ttl_time(user_id)
                        house = ttl_seconds // 3600
                        seconds_remainder = ttl_seconds - (house*3600)
                        minutes = seconds_remainder // 60
                        seconds = seconds_remainder - (minutes * 60)

                        await event.delete()
                        return await event.answer(text=f'Download limit for today is exhausted\n\nBuy coins or come back in {house-1} hours, {minutes} minutes, {seconds} seconds')
                    
                    else:
                        await event.answer(text=f'You use 1 coin\nCoins left {count_user_coins-1}\n\nWait for the file to load')
                        await User.update_coins(user_id, coins=count_user_coins-1)
                        return await handler(event, data)
                    
                else:
                    await downloader.add_user_in_cache(user_id)
                    if count_user_coins != 0:
                        await event.answer(text='Attention free download limit for today is over, further selection of tracks will charge 1 coin')

            return await handler(event, data)