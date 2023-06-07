from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database.tables.users import get_user_inner_id
from gui.displays.displays import MenuDisplay, MenuEtcDisplay, MenuEtcNoteNameDisplay
from gui.keyboards.keyboards import MenuKeyboard, MenuEtcKeyboard, MenuEtcNoteNameKeyboard
from machine.actions import delete_note
from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

__all__ = [
            'menu_key', 
            'menu_etc_key',
            'menu_etc_note_name_key',
          ]

@is_user(1)
async def menu_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(call.from_user.id, "tg")
    delete_note(user_id)
    await state.finish()
    await return_message(update=call, text=MenuDisplay(), keyboard=MenuKeyboard())
        
           
@is_user(2)
async def menu_etc_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(call.from_user.id, "tg")
    delete_note(user_id)
    await state.finish()
    await return_message(update=call, text=MenuEtcDisplay(), keyboard=MenuEtcKeyboard())
        
    
@is_user(2)
async def menu_etc_note_name_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await state.set_state("menu.etc.note.name")
    await return_message(update=call, text=MenuEtcNoteNameDisplay(), keyboard=MenuEtcNoteNameKeyboard())