from aiogram import Bot,Dispatcher
import sys, logging
from aiogram.client.bot import DefaultBotProperties
from .handler import setup_routers
from config.settings import BOT_TOKEN


async def on_startup(bot):
    print('bot ishladi')

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    ds = Dispatcher()
    router = await setup_routers()
    ds.include_router(router)
    
    try:
        ds.startup.register(on_startup)
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        await ds.start_polling(bot)
    except:
        pass
