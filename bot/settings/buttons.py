from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def CreateInline(*button_rows, just=(1,)) -> InlineKeyboardMarkup: #! {a: a, b: b}
    builder = InlineKeyboardBuilder()
    for row in button_rows:
        for text, callback_data in row.items():
            if callback_data.startswith('https:'):
                builder.add(InlineKeyboardButton(text=text,url=callback_data))
            else:
                builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(*just)
    return builder.as_markup()


def Createreply(*args, contact=False, just=(2,)) -> ReplyKeyboardBuilder: #! 'a', 'b', ..
    bulder = ReplyKeyboardBuilder()
    for i in args:
        bulder.add(KeyboardButton(text=i, request_contact=True if contact else False))
    bulder.adjust(*just)
    return bulder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        