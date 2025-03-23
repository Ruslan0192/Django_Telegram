import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands.com_menu import private

from handlers.user import user_router, def_timer_dispatch

from database.middleware import DataBaseSession
from database.engine import session_maker, engine, async_sessionmaker, AsyncSession


from config import settings, logger


bot = Bot(token=settings.TOKEN_TG)
bot.my_admins_list = []
bot.supeadmin = 0

scheduler = AsyncIOScheduler()

storage = RedisStorage.from_url(settings.REDIS_URL)
dp = Dispatcher(storage=storage)
# dp = Dispatcher()
dp.include_router(user_router)

TIME_DISPATCH = 60


async def on_startup():
    if not os.path.exists('logging'):
        os.mkdir('logging')

    session_scheduler = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    scheduler.start()
    scheduler.add_job(func=def_timer_dispatch,
                      trigger='interval',
                      seconds=TIME_DISPATCH,
                      args=(session_scheduler(), bot))

    logger.info("Бот успешно запущен!", telegram_id=0)


async def on_shutdown():
    logger.critical("Бот остановился!", user_id=0)


async def main():
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
