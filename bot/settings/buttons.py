import os
from aiogram import Bot
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config.settings import BOT_TOKEN
from collections import defaultdict
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, 
    FSInputFile, Poll)
from django.core.files.storage import default_storage
from asgiref.sync import sync_to_async


async def send_messages_to_groups(bot_message):
    bot_token = BOT_TOKEN
    bot = Bot(token=bot_token)

    groups = await sync_to_async(lambda: list(bot_message.to_group.all()), thread_sensitive=True)()
    if not groups:
        print("❌ Нет групп для отправки")
        return

    text = bot_message.message_text
    buttons = await sync_to_async(lambda: list(bot_message.buttons.all()), thread_sensitive=True)()

    if not buttons:
        print("❌ Variantlar topilmadi")
        return
    
    options = [button.text for button in buttons]
    correct_option_index = next((i for i, btn in enumerate(buttons) if btn.is_correct), None)

    for group in groups:
        group_chat_id = group.group_id

        await bot.send_poll(
            chat_id=group_chat_id,
            question=text,
            options=options,
            type='regular',
            correct_option_id=correct_option_index,
            is_anonymous=bot_message.static,
            allows_multiple_answers=False
        )


def CreateInline(*button_rows, just=(1,)) -> InlineKeyboardMarkup:  #! {a: a, b: b}
    builder = InlineKeyboardBuilder()
    for row in button_rows:
        for text, callback_data in row.items():
            if callback_data.startswith('https:'):
                builder.add(InlineKeyboardButton(text=text,url=callback_data))
            else:
                builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(*just)
    return builder.as_markup()


def Createreply(*args, contact=False, just=(2,)) -> ReplyKeyboardBuilder:  #! 'a', 'b', ..
    bulder = ReplyKeyboardBuilder()
    for i in args:
        bulder.add(KeyboardButton(text=i, request_contact=True if contact else False))
    bulder.adjust(*just)
    return bulder.as_markup(resize_keyboard=True, one_time_keyboard=True)


# async def send_messages_to_groups(bot_message):
#     bot_token = BOT_TOKEN
#     bot = Bot(token=bot_token)

#     groups = await sync_to_async(lambda: list(bot_message.to_group.all()), thread_sensitive=True)()
#     if not groups:
#         print("❌ Нет групп для отправки")
#         return

#     text = bot_message.message_text
#     buttons = await sync_to_async(lambda: list(bot_message.buttons.all()), thread_sensitive=True)()

#     for group in groups:
#         group_chat_id = group.group_id

#         keyboard_rows = defaultdict(list)
#         for button in buttons:
#             keyboard_rows[button.row].append(button)

#         reply_markup = None
#         if buttons:
#             keyboard = [
#                 [InlineKeyboardButton(
#                     text=btn.text, 
#                     callback_data=f"answer_{group_chat_id}_{btn.id}_{'none'}"  #! btn.callback_data qo'shish
#                 ) for btn in sorted(keyboard_rows[row], key=lambda btn: btn.position)]
#                 for row in sorted(keyboard_rows.keys())
#             ]
#             reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

#         if bot_message.photo:
#             photo_path = await sync_to_async(default_storage.path, thread_sensitive=True)(bot_message.photo.name)
#             exists = await sync_to_async(os.path.exists)(photo_path)
#             if exists:
#                 photo = FSInputFile(photo_path)
#                 await bot.send_photo(chat_id=group_chat_id, photo=photo, caption=text, reply_markup=reply_markup)
#             else:
#                 await bot.send_message(chat_id=group_chat_id, text=f"Ошибка: файл {photo_path} не найден.", reply_markup=reply_markup)
#         else:
#             await bot.send_message(chat_id=group_chat_id, text=text, reply_markup=reply_markup)