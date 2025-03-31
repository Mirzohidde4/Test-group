from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class GroupFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]