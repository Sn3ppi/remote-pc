from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.tables.users import get_user_inner_id
from gui.displays.displays import MenuDisplay, MenuEtcDisplay
from gui.keyboards.keyboards import MenuKeyboard, MenuEtcKeyboard
from machine.actions import delete_note, name_note
from models.tg.tools.return_message import return_message
from models.tg.tools.is_user import is_user

@is_user(1)
async def menu_command(message: Message, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(message.from_user.id, "tg")
    delete_note(user_id)
    await state.finish()
    await return_message(message, text=MenuDisplay(), keyboard=MenuKeyboard())


@is_user(2)
async def menu_etc_note_name_command(message: Message, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(message.from_user.id, "tg")
    name_note(user_id, message.text)
    await state.finish()
    await return_message(message, text=MenuEtcDisplay(), keyboard=MenuEtcKeyboard())