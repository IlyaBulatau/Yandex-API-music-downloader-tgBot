from aiogram import Bot, Dispatcher
import asyncio

from handlers.commands import router as router_commands

from documents.menu import set_commands_menu
from database.connect import db
from database.models import User, Base
from config import config
from logger.logger import logger

async def main():

    bot = Bot(token=config.BOT_TOKEN)
    ds = Dispatcher()

    ds.include_routers(router_commands,)
    
    await db.create_db()
    await db.create_models(Base.metadata)

    await bot(set_commands_menu())
    await ds.start_polling(bot)


if __name__ == "__main__":
    logger.warning('START BOT')
    asyncio.run(main())