import logging, asyncio
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from main.models import UserAnswer, InlineButton
from asgiref.sync import sync_to_async


group_router = Router()

@group_router.message(CommandStart())
async def group_messages(message: Message):
    await message.answer(text="group")


@group_router.callback_query(lambda call: call.data.startswith("answer_"))
async def handle_answer(call: CallbackQuery):
    # Callback data: answer_{group_id}_{button_id}_{callback_data}
    data_parts = call.data.split("_")
    group_id = data_parts[1]
    button_id = data_parts[2]
    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.full_name

    button = await sync_to_async(InlineButton.objects.get, thread_sensitive=True)(id=button_id)

    await sync_to_async(UserAnswer.objects.create, thread_sensitive=True)(
        user_id=user_id, username=username, group_id=group_id,
        button=button, is_correct=button.is_correct)
   
    await call.answer(button.text_response)
    