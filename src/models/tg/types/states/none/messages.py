from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from gui.displays.displays import MenuDisplay
from gui.keyboards.keyboards import MenuKeyboard
from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

@is_user(1)
async def menu_command(message: Message, state: FSMContext, *args, **kwargs) -> None:
    await return_message(message, text=MenuDisplay(), keyboard=MenuKeyboard())