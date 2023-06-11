from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.tables.users import get_user_data
from gui.displays.displays import MenuDisplay
from gui.displays.messages import *
from gui.keyboards.keyboards import MenuKeyboard
from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

__all__ = [
    'menu_command',
    'user_data'
]

@is_user(1)
async def menu_command(message: Message, state: FSMContext, *args, **kwargs) -> None:
    await return_message(message, text=MenuDisplay(), keyboard=MenuKeyboard())
    
    
@is_user(2)
async def user_data(message: Message, state: FSMContext, *args, **kwargs) -> None:
    account_type = "tg"
    if message.reply_to_message:
        user_id = str(message.reply_to_message.from_user.id)
    else:
        user_id = str(message.from_user.id)    
    data = get_user_data(user_id, account_type)
    await return_message(message, text=UserProfile(data, user_id, account_type))