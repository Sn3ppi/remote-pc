from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from database.tables.users import get_user_inner_id
from gui.displays.displays import MenuDisplay, MenuEtcDisplay
from gui.keyboards.keyboards import MenuKeyboard, MenuEtcKeyboard
from machine.actions import delete_note
from models.tg.tools.return_message import return_message
from models.tg.tools.is_user import is_user

__all__ = [
            'menu_key', 
            'menu_etc_key'
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