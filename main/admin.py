from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin, StackedInline


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


class InlineButtons(StackedInline):
    model = InlineButton
    extra = 1
    fields = ['text', 'text_response', 'is_correct', 'static']
    ordering_field = ['text']


@admin.register(BotMessage)
class AdminBotMessage(ModelAdmin):
    list_display = ('message_text', 'to_group')    
    inlines = [InlineButtons]
