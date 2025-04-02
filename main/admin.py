from django.contrib import admin
from .models import *
import os
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin, StackedInline
from asgiref.sync import sync_to_async, async_to_sync
from config.settings import BOT_TOKEN
from aiogram import Bot
from collections import defaultdict
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from django.core.files.storage import default_storage


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(UserMod)
class AdminUserMod(ModelAdmin):
    list_display = ('user_name', 'full_name')


@admin.register(AdminMod)
class AdminAdminMod(ModelAdmin):
    list_display = ('user_name', 'full_name')

    def has_add_permission(self, request):
        if AdminMod.objects.count() >= 1:
            return False
        else:
            return True
        

@admin.register(GroupMod)
class AdminGroupMod(ModelAdmin):
    list_display = ('group_name', 'group_id')   
    search_fields = ('group_name', 'group_id')     


class InlineButtons(StackedInline):
    model = InlineButton
    extra = 1
    fields = ['text', 'text_response', 'row', 'position', 'is_correct', 'static']
    ordering_field = ['text']



async def send_messages_to_groups(bot_message):
    bot_token = BOT_TOKEN
    bot = Bot(token=bot_token)
    print(bot_message)

    groups = await sync_to_async(lambda: list(bot_message.to_group.all()), thread_sensitive=True)()
    if not groups:
        print("❌ Нет групп для отправки")
        return

    text = bot_message.message_text
    buttons = await sync_to_async(lambda: list(bot_message.buttons.all()), thread_sensitive=True)()

    for group in groups:
        group_chat_id = group.group_id

        keyboard_rows = defaultdict(list)
        for button in buttons:
            keyboard_rows[button.row].append(button)

        reply_markup = None
        if buttons:
            keyboard = [
                [InlineKeyboardButton(
                    text=btn.text, 
                    callback_data=f"answer_{group_chat_id}_{btn.id}_{'none'}" #! btn.callback_data qo'shish
                ) for btn in sorted(keyboard_rows[row], key=lambda btn: btn.position)]
                for row in sorted(keyboard_rows.keys())
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        if bot_message.photo:
            photo_path = await sync_to_async(default_storage.path, thread_sensitive=True)(bot_message.photo.name)
            exists = await sync_to_async(os.path.exists)(photo_path)
            if exists:
                photo = FSInputFile(photo_path)
                await bot.send_photo(chat_id=group_chat_id, photo=photo, caption=text, reply_markup=reply_markup)
            else:
                await bot.send_message(chat_id=group_chat_id, text=f"Ошибка: файл {photo_path} не найден.", reply_markup=reply_markup)
        else:
            await bot.send_message(chat_id=group_chat_id, text=text, reply_markup=reply_markup)


@admin.action(description="Send to groups")
def send_to_group(modeladmin, request, queryset):
    """Отправка сообщений в группу из Django Admin"""
    for bot_message in queryset:
        async_to_sync(send_messages_to_groups)(bot_message)


@admin.register(BotMessage)
class AdminBotMessage(ModelAdmin):
    list_display = ('message_text',)    
    inlines = [InlineButtons]
    actions = [send_to_group]
    
    def display_groups(self, obj):
        return ', '.join([group.name for group in obj.to_group.all()])
    
    display_groups.short_description = 'Guruhlar'
    autocomplete_fields = ['to_group']
