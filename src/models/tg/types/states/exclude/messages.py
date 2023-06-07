from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from machine.randomizer import random_mention
from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

__all__ = [
    'username'
]
    
@is_user(1)
async def username(message: Message, state: FSMContext, *args, **kwargs) -> None:
    bot = await message.from_user.bot.me
    if f"@{bot.username}" in message.text:
        message_type, message_text = random_mention()
        if message_type == 'sticker':
            await return_message(message, sticker=message_text)
        elif message_type == 'emoji':
            await return_message(message, text=message_text)