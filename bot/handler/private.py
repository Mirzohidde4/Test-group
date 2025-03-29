import django, os
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from asgiref.sync import sync_to_async
from main.models import UserMod
from ..settings.states import UserState
from ..settings.buttons import CreateInline, Createreply


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
user_private_router = Router()


@user_private_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await message.answer(f'Salom {message.from_user.full_name}')
