from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin, StackedInline
from asgiref.sync import async_to_sync
from bot.settings.buttons import send_messages_to_groups


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(UserMod)
class AdminUserMod(ModelAdmin):
    list_display = ('user_name', 'full_name')
    search_fields = ('user_name', 'full_name')


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
    fields = ['text', 'text_response', 'is_correct']
    ordering_field = ['text']


@admin.action(description="Jo'natish")
def send_to_group(modeladmin, request, queryset):
    """Отправка сообщений в группу из Django Admin"""
    for bot_message in queryset:
        async_to_sync(send_messages_to_groups)(bot_message)


@admin.register(BotMessage)
class AdminBotMessage(ModelAdmin):
    list_display = ('message_text', 'static')    
    list_filter = ('static',)
    inlines = [InlineButtons]
    actions = [send_to_group]
    
    def display_groups(self, obj):
        return ', '.join([group.name for group in obj.to_group.all()])
    
    display_groups.short_description = 'Guruhlar'
    autocomplete_fields = ['to_group']


@admin.register(UserAnswer)
class UserAnswerAdmin(ModelAdmin):
    list_display = ("username", "group_id", "button", "is_correct", "created_at")
    list_filter = ("is_correct", "group_id", 'created_at')
    search_fields = ("username",)