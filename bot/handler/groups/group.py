import logging, asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext


group_router = Router()

@group_router.message(CommandStart())
async def group_messages(message: Message):
    await message.answer(text="group")
