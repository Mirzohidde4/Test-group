import logging, asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


admin_router = Router()


@admin_router.message(Command('admin'))
async def get_all_users(message: Message):
    await message.answer(text='you are admin')
