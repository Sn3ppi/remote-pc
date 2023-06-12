from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from gui.displays.displays import MenuDisplay
from gui.displays.messages import *
from gui.keyboards.keyboards import MenuKeyboard
from models.tg.tools.is_user import is_user
from models.tg.tools.user_data import get_user_id_by_message_type
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
    data = get_user_id_by_message_type(message)
    if data is not None and data:
        await return_message(message, text=UserProfile(data))