from aiogram.dispatcher.filters.filters import BoundFilter
from aiogram.types import CallbackQuery
from dispatcher import dp


class IsChannelFilter(BoundFilter):
    key = 'is_channel'

    def __init__(self, is_channel):
        self.is_channel = is_channel

    async def check(self, call: CallbackQuery) -> bool:
        is_channel = call.message.chat.type == 'channel'
        if self.is_channel:
            return is_channel
        return not is_channel


class IsContactFilter(BoundFilter):
    key = 'is_contact'

    def __init__(self, is_contact):
        self.is_contact = is_contact

    async def check(self, call: CallbackQuery) -> bool:
        data = call.data.split()
        if len(data) == 2:
            try:
                int(data[1])
                return True
            except ValueError:
                return False
        return False


if __name__ == 'filters':
    dp.filters_factory.bind(IsChannelFilter)
    dp.filters_factory.bind(IsContactFilter)
