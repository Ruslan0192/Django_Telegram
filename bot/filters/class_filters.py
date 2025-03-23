import os

from aiogram.filters import Filter, BaseFilter
from aiogram import Bot, types


# class ChatTypeFilter(Filter):
#     def __init__(self, chat_types: list[str]) -> None:
#         self.chat_types = chat_types
#
#     async def __call__(self, message: types.Message) -> bool:
#         return message.chat.type in self.chat_types

class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admins_list


class IsUser(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id not in bot.my_admins_list
