from aiogram import Dispatcher
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation, MessageNotModified, RetryAfter

from models.tg.types.states.none.handlers import none_handlers
from models.tg.types.states.note.handlers import note_handlers
from models.tg.types.states.note_name.handlers import note_name_handlers
from models.tg.types.states.exclude.handlers import exclude_handlers
from models.tg.types.errors import *

def register_handlers(dp: Dispatcher) -> None:
    dp.register_errors_handler(bot_blocked, exception=BotBlocked)
    dp.register_errors_handler(cant_initiate_conversation, exception=CantInitiateConversation)
    dp.register_errors_handler(message_not_modified, exception=MessageNotModified)
    dp.register_errors_handler(flood_wait_retry_after, exception=RetryAfter)
    note_name_handlers(dp)
    note_handlers(dp)
    none_handlers(dp)
    exclude_handlers(dp)