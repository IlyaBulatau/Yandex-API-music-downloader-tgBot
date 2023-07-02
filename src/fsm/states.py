from aiogram.fsm.state import State, StatesGroup


class MusicState(StatesGroup):
    id = State()

class PaymentState(StatesGroup):
    count = State()
