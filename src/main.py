from aiogram import Bot, Dispatcher

from config import config
import asyncio

from handlers.commands import router as router_commands

from documents.menu import set_commands_menu

async def main():

    bot = Bot(token=config.BOT_TOKEN)
    ds = Dispatcher()

    ds.include_routers(router_commands,)

    await bot.set_my_commands(set_commands_menu())
    await ds.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())