from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    order = State()
    location = State()
    tariff = State()
    confirm = State()
    search = State()

    # registration
    contact = State()
