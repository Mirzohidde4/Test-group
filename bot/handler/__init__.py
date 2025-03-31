from aiogram import Router
from bot.filters.channel import ChannelFilter
from bot.filters.private_chat import ChatPrivateFilter
from bot.filters.group import GroupFilter
from bot.filters.admin import IsBotAdminFilter
from main.models import AdminMod
from asgiref.sync import sync_to_async


async def get_admin_id():
    """Bazadan admin ID'sini asinxron olish"""
    return await sync_to_async(lambda: AdminMod.objects.first())()


async def setup_routers() -> Router:
    from .users import private
    from .groups import group
    from .channels import channel
    from .admin import admin
    
    router = Router()
    admin_obj = await get_admin_id()
    admin_id = admin_obj.user_id if admin_obj else None  

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    private.user_private_router.message.filter(ChatPrivateFilter(is_private=True))
    group.group_router.message.filter(GroupFilter())
    admin.admin_router.message.filter(IsBotAdminFilter(admin_id=admin_id))
    channel.channel_router.message.filter(ChannelFilter())

    router.include_routers(private.user_private_router, group.group_router, channel.channel_router, admin.admin_router)
    return router