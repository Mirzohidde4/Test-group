import asyncio
from django.core.management.base import BaseCommand

from bot.main import main

class Command(BaseCommand):
    help = 'Telegram botni ishga tushirish'

    def handle(self, *args, **kwargs):
        asyncio.run(main())