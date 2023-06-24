from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand

def set_commands_menu():
    commands = SetMyCommands(commands=[
        BotCommand(command='start', description='Start over'),
    ])

    return commands