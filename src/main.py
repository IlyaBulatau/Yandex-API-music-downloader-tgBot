from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

from handlers.commands import router as router_commands
from handlers.callback import router as router_callbacks
from handlers.inline import router as router_inline

from documents.menu import set_commands_menu
from database.connect import db
from database.models import User, Base
from config import config
from logger.logger import logger
from services.music_api import music_api
from fsm.cache import redis

async def main():

    bot = Bot(token=config.BOT_TOKEN)
    storage = RedisStorage(redis=redis)
    ds = Dispatcher(storage=storage)

    ds.include_routers(router_commands,
                       router_callbacks,
                       router_inline)

    await db.create_db()
    await db.create_models(Base.metadata)

    await music_api.client.init()

    await bot(set_commands_menu())
    await ds.start_polling(bot)


if __name__ == "__main__":
    logger.warning('START BOT')
    asyncio.run(main())

# TODO - отефакторить взаимодействие с ботом
# TODO - сделать загрузки аудио быстрее
# TODO - сделать лимит на скачивание песен
# TODO - сделать возможнотсть покупки монет для скачивания песен без лимита
# TODO - добавить интернализацию
