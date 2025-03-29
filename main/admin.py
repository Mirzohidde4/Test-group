from django.contrib import admin
from .models import UserMod
from django.contrib.auth.models import User, Group


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(UserMod)
class AdminUserMod(admin.ModelAdmin):
    list_display = ('user_name', 'full_name')