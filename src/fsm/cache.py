from aiogram.fsm.storage.redis import Redis

from config import config

redis = Redis(host=config.REDIS_HOST)
