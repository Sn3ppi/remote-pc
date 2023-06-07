from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound, BotBlocked, CantInitiateConversation, NetworkError

from database.tables.users import get_users_of_level

async def notify_users(bot: Bot, power=True) -> None:
    '''Отправляет уведомление о запуске бота.'''
    notify_users = get_users_of_level("tg", 4)
    if notify_users is not None:
        if power:
            text = "👋"
        else:
            text = "😴"
        for user_id in notify_users:
            try:
                await bot.send_message(chat_id=user_id[0], text=text)
            except (ChatNotFound, BotBlocked, CantInitiateConversation, NetworkError):
                return