from aiogram.fsm.storage.redis import Redis

from config import config
from datetime import datetime, timedelta


redis = Redis(host=config.REDIS_HOST)


class Downloader:
    """
    Отвечает за хэш загрузки файлов юзером
    """

    def __init__(self):
        self.cache = redis

    
    async def add_user_in_cache(self, user_id):
        """
        Добавляет юзера в кэш на время до окнчания дня (до 00:00)
        """
        time_now = datetime.now() # текущее время
        time_now_in_seconds = (time_now.hour*60*60) + (time_now.minute*60) + time_now.second # текущее время в секундах
        seconds_in_day = 24*60*60 # всего секунд в 1 дне
        time_until_the_end_of_the_download_limit = seconds_in_day-time_now_in_seconds # время кэша до конца дня

        await self.cache.set(user_id, 'limit', ex=time_until_the_end_of_the_download_limit)

    async def is_a_user_limit(self, user_id):
        """
        Проверяет есть ли юзер в кэше

        Если есть возвращает True
        """
        get_result = await self.cache.get(user_id)
        if get_result != None:
            return True
        return False
    
    async def get_user_ttl_time(self, user_id):
        """
        Возвращает ttl кэша юзера - сколько времени осталось до удаления из кэша
        """
        return await self.cache.ttl(user_id)


downloader = Downloader()
