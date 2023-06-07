from asyncio import sleep
from aiogram.types import Update
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation, MessageNotModified, RetryAfter

__all__ = ['bot_blocked', 'cant_initiate_conversation', 'message_not_modified', 'flood_wait_retry_after']

async def bot_blocked(update: Update, exception: BotBlocked) -> bool:
    return True


async def cant_initiate_conversation(update: Update, exception: CantInitiateConversation) -> bool:
    return True


async def message_not_modified(update: Update, exception: MessageNotModified) -> bool:
    await update.callback_query.answer()
    return True


async def flood_wait_retry_after(update: Update, exception: RetryAfter) -> bool:
    await sleep(exception.timeout)
    return True