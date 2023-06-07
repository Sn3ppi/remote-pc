from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database.tables.users import get_user_inner_id
from gui.displays.displays import MenuDisplay, MenuEtcNoteDisplay
from gui.keyboards.keyboards import MenuKeyboard, MenuEtcNoteKeyboard
from machine.actions import *
from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

@is_user(1)
async def menu_command(message: Message, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(message.from_user.id)
    delete_note(user_id)
    await state.finish()
    await return_message(message, text=MenuDisplay(), keyboard=MenuKeyboard())


@is_user(2)
async def menu_etc_note_command(message: Message, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(message.from_user.id, "tg")
    write_note(user_id, message.text)
    await return_message(message, text=MenuEtcNoteDisplay(), keyboard=MenuEtcNoteKeyboard())