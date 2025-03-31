from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatPrivateFilter(BaseFilter):
    def __init__(self, is_private: bool = True):
        self.is_private = is_private

    async def __call__(self, message: Message) -> bool:
        return (message.chat.type == ChatType.PRIVATE) == self.is_private
