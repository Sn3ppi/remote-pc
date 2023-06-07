from math import ceil
import re

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.folders import get_favorites_count, get_favorites_page
from app.config.tmp import stop_sig
from database.tables.users import get_user_inner_id, get_users, get_users_count, set_level
from database.tables.machine import (
    get_net_autoupdate_frequency, 
    get_sys_autoupdate_frequency, 
    update_net_autoupdate_frequency, 
    update_sys_autoupdate_frequency,
)
from database.tables.stats import get_network, get_sensors
from gui.displays.displays import *
from gui.keyboards.keyboards import *
from machine.actions import *
from models.tg.tools.is_user import is_user
from models.tg.tools.return_message import return_message

__all__ = [
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
            'menu_etc_screen_key',
            'menu_about'
          ]

@is_user(1)
async def menu_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuDisplay(), keyboard=MenuKeyboard())
        

@is_user(1)
async def menu_sys_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuSysDisplay(get_sensors()), keyboard=MenuSysKeyboard())
        

@is_user(1)
async def menu_net_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuNetDisplay(get_network()), keyboard=MenuNetKeyboard())
        
    
@is_user(3)
async def menu_progs_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(
        update=call,
        text=MenuProgsDisplay(),
        keyboard=MenuProgsKeyboard(
            generator=get_favorites_page,
            count=get_favorites_count()
        )
    )
          

@is_user(3)
async def menu_progs_id_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    programm_id = int(re.search(r'id_(\d+)', call.data).group(1)) 
    start_app(programm_id)
    await return_message(
        update=call,
        text=MenuProgsDisplay(),
        keyboard=MenuProgsKeyboard(
            generator=get_favorites_page,
            count=get_favorites_count()
        )
    )  


@is_user(3)
async def menu_opts_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuOptsDisplay(), keyboard=MenuOptsKeyboard())
        

@is_user(3)
async def menu_opts_machine_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuOptsMachineDisplay(), keyboard=MenuOptsMachineKeyboard())
        
    
@is_user(3)
async def menu_opts_machine_sys_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    frequency = ceil(get_sys_autoupdate_frequency() / 60)
    await return_message(update=call, text=MenuOptsMachineSysDisplay(), keyboard=MenuOptsMachineSysKeyboard(frequency))
        
    
@is_user(3)
async def menu_opts_machine_sys_plus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    update_sys_autoupdate_frequency(True)
    frequency = ceil(get_sys_autoupdate_frequency() / 60) 
    await return_message(update=call, text=MenuOptsMachineSysDisplay(), keyboard=MenuOptsMachineSysKeyboard(frequency))
        
        
@is_user(3)
async def menu_opts_machine_sys_minus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    update_sys_autoupdate_frequency(False)
    frequency = ceil(get_sys_autoupdate_frequency() / 60) 
    await return_message(update=call, text=MenuOptsMachineSysDisplay(), keyboard=MenuOptsMachineSysKeyboard(frequency))
        

@is_user(3)
async def menu_opts_machine_net_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    frequency = ceil(get_net_autoupdate_frequency() / 60)
    await return_message(update=call, text=MenuOptsMachineNetDisplay(), keyboard=MenuOptsMachineNetKeyboard(frequency))
        
    
@is_user(3)
async def menu_opts_machine_net_plus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    update_net_autoupdate_frequency(True)
    frequency = ceil(get_net_autoupdate_frequency() / 60) 
    await return_message(update=call, text=MenuOptsMachineNetDisplay(), keyboard=MenuOptsMachineNetKeyboard(frequency))
        
       
@is_user(3) 
async def menu_opts_machine_net_minus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    update_net_autoupdate_frequency(False)
    frequency = ceil(get_net_autoupdate_frequency() / 60) 
    await return_message(update=call, text=MenuOptsMachineNetDisplay(), keyboard=MenuOptsMachineNetKeyboard(frequency))
        

@is_user(3) 
async def menu_opts_machine_reboot_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
    pc_reboot()
        
        
@is_user(3)
async def menu_opts_machine_off_key(call: CallbackQuery, *args, **kwargs) -> None: 
    await call.answer()
    pc_off()
    

@is_user(3)
async def menu_opts_bot_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuOptsBotDisplay(), keyboard=MenuOptsBotKeyboard())
        
    
@is_user(3)
async def menu_opts_bot_off_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await call.answer()
    stop_sig.set()


@is_user(3)
async def menu_opts_bot_log_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    logs = get_logs()
    if logs is not None:
        await return_message(update=call, document=logs)
        await return_message(update=call, text=MenuOptsBotDisplay(), keyboard=MenuOptsBotKeyboard(), condition=False)
    else:
        await call.answer()

    
@is_user(3)
async def menu_opts_access_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(
        update=call, 
        text=MenuOptsAccessDisplay(), 
        keyboard=MenuOptsAccessKeyboard(
            generator=get_users,
            count=get_users_count()[0][0]       
        )   
    )
        

@is_user(3)
async def menu_opts_access_plus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    user_id = int(re.search(r'id_(\d+)', call.data).group(1)) 
    set_level(True, user_id)
    await return_message(
        update=call, 
        text=MenuOptsAccessDisplay(), 
        keyboard=MenuOptsAccessKeyboard(
            generator=get_users,
            count=get_users_count()[0][0]       
        )
    )
            
        
@is_user(3)
async def menu_opts_access_minus_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    user_id = int(re.search(r'id_(\d+)', call.data).group(1)) 
    set_level(False, user_id)
    await return_message(
        update=call, 
        text=MenuOptsAccessDisplay(), 
        keyboard=MenuOptsAccessKeyboard(
            generator=get_users,
            count=get_users_count()[0][0]       
        )
    )
            
        
@is_user(2)
async def menu_etc_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuEtcDisplay(), keyboard=MenuEtcKeyboard())
        
        
@is_user(2)
async def menu_etc_note_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(call.from_user.id, "tg")
    write_note(user_id, "")
    await state.set_state("menu.etc.note")
    await return_message(update=call, text=MenuEtcNoteDisplay(), keyboard=MenuEtcNoteKeyboard())
    
    
@is_user(3)
async def menu_etc_screen_key(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    user_id = get_user_inner_id(call.from_user.id, "tg")
    document = screenshot(user_id)
    if document is not None:
        await return_message(update=call, document=document)
        await return_message(update=call, text=MenuEtcDisplay(), keyboard=MenuEtcKeyboard(), condition=False)
    else:
        await call.answer()
    
    
@is_user(1)
async def menu_about(call: CallbackQuery, state: FSMContext, *args, **kwargs) -> None:
    await return_message(update=call, text=MenuAboutDisplay(), keyboard=MenuAboutKeyboard())