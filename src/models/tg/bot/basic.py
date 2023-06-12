from threading import Thread

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import ChatNotFound, ChatIdIsEmpty, Unauthorized, ValidationError, NetworkError
import asyncio

from app.config.tmp import stop_sig
from app.log import logger
from app.register import get_tg_bot_token, reset_tg_bot_token, get_tg_admin_id, reset_tg_admin_id
from database.tables.users import get_user_level, add_user, set_needed_level
from models.tg.tools.notify_list import notify_users
from models.tg.types import register_handlers

class TGBotBasic(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name = "TG Bot"
        self._loop = asyncio.new_event_loop()
        
    async def _on_startup(self, dp: Dispatcher) -> None:
        try:
            admin_id = get_tg_admin_id()
            await dp.bot.get_chat(admin_id)
            register_handlers(dp=dp)
            user_level = get_user_level(admin_id, "tg")  
            if user_level is None: 
                add_user(user_id=admin_id, account_type="tg")
            set_needed_level(access_level=4, user_id=admin_id, account_type="tg")
            await notify_users(dp.bot, True)
            logger.info("Бот запущен!")
        except (ChatNotFound, ChatIdIsEmpty):
            reset_tg_admin_id()
            stop_sig.set()
        except (NetworkError):
            stop_sig.set()
            
    async def _on_shutdown(self, dp: Dispatcher) -> None:
        logger.info("Бот выключен.")
        try:
            if dp is not None:
                await notify_users(dp.bot, False)
        except (NetworkError):
            return
        
    def stop(self) -> None:
        tasks = [task for task in asyncio.all_tasks(loop=self._loop)]
        for task in tasks:
            if task is not asyncio.current_task(loop=self._loop):
                task.cancel()
        self._loop.call_soon_threadsafe(self._loop.stop)
        
    def run(self) -> None:
        bot_token = get_tg_bot_token()
        if bot_token is not None:
            try:
                bot = Bot(token=bot_token, parse_mode="HTML")
                dp = Dispatcher(bot=bot, storage=MemoryStorage())
                asyncio.set_event_loop(loop=self._loop)
                executor.start_polling(
                    loop=self._loop,
                    on_startup=self._on_startup,
                    on_shutdown=self._on_shutdown,
                    dispatcher=dp,
                    skip_updates=True
                )
                self._loop.close()
            except (Unauthorized, ValidationError):
                reset_tg_bot_token()
                stop_sig.set()
            except (NetworkError):
                stop_sig.set()