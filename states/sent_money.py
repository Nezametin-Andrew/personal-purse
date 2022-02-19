from aiogram.dispatcher.filters.state import State, StatesGroup


class SentMoney(StatesGroup):
    coin = State()
    address = State()
