from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

__all__ = [
            'zero_key',
            'menu_key', 
            'menu_sys_key', 
            'menu_net_key', 
            'menu_progs_key',
            'menu_progs_id_key',
            'menu_opts_key', 
            'menu_opts_machine_key', 
            'menu_opts_machine_sys_key', 
            'menu_opts_machine_sys_plus_key',
            'menu_opts_machine_sys_minus_key',
            'menu_opts_machine_net_key',
            'menu_opts_machine_net_plus_key',
            'menu_opts_machine_net_minus_key',
            'menu_opts_machine_reboot_key',
            'menu_opts_machine_off_key',
            'menu_opts_bot_key',
            'menu_opts_bot_off_key',
            'menu_opts_bot_log_key',
            'menu_opts_access_key',
            'menu_opts_access_plus_key',
            'menu_opts_access_minus_key',
            'menu_etc_key',
            'menu_etc_note_key',
            'menu_etc_note_name_key',
            'menu_etc_screen_key',
            'menu_about',
          ]

async def zero_key(call: CallbackQuery, *args, **kwargs) -> None:
    await call.answer()


@is_user(1)
async def menu_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        

@is_user(1)
async def menu_sys_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        

@is_user(1)
async def menu_net_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
    
@is_user(3)
async def menu_progs_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
          

@is_user(3)
async def menu_progs_id_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()


@is_user(3)
async def menu_opts_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        

@is_user(3)
async def menu_opts_machine_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
    
@is_user(3)
async def menu_opts_machine_sys_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
    
@is_user(3)
async def menu_opts_machine_sys_plus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
        
@is_user(3)
async def menu_opts_machine_sys_minus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        

@is_user(3)
async def menu_opts_machine_net_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
    
@is_user(3)
async def menu_opts_machine_net_plus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
       
@is_user(3) 
async def menu_opts_machine_net_minus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        

@is_user(3) 
async def menu_opts_machine_reboot_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
        
@is_user(3)
async def menu_opts_machine_off_key(call: CallbackQuery, *args, **kwargs) -> None: 
    await call.answer()
    

@is_user(3)
async def menu_opts_bot_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
    
@is_user(3)
async def menu_opts_bot_off_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
         

@is_user(3)
async def menu_opts_bot_log_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()

    
@is_user(3)
async def menu_opts_access_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        

@is_user(3)
async def menu_opts_access_plus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
            
        
@is_user(3)
async def menu_opts_access_minus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
            
        
@is_user(2)
async def menu_etc_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
        
        
@is_user(2)
async def menu_etc_note_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
    

@is_user(2)
async def menu_etc_note_name_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
       

@is_user(3)
async def menu_etc_screen_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
    

@is_user(1)
async def menu_about(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()