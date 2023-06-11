from aiogram import Dispatcher

from models.tg.types.states.none.buttons import *
from models.tg.types.states.none.messages import *

def none_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(menu_key, state=None, regexp="menu.pg_[0-9]+")
    dp.register_callback_query_handler(menu_sys_key, state=None, regexp="menu.sys.pg_[0-9]+")
    dp.register_callback_query_handler(menu_net_key, state=None, regexp="menu.net.pg_[0-9]+")
    dp.register_callback_query_handler(menu_progs_key, state="*", regexp="menu.progs.pg_[0-9]+")
    dp.register_callback_query_handler(menu_progs_id_key, state="*", regexp="menu.progs.id_[0-9]+.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_key, state=None, regexp="menu.opts.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_key, state=None, regexp="menu.opts.machine.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_sys_key, state=None, regexp="menu.opts.machine.sys.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_sys_plus_key, state=None, regexp="menu.opts.machine.sys.plus.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_sys_minus_key, state=None, regexp="menu.opts.machine.sys.minus.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_net_key, state=None, regexp="menu.opts.machine.net.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_net_plus_key, state=None, regexp="menu.opts.machine.net.plus.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_net_minus_key, state=None, regexp="menu.opts.machine.net.minus.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_machine_reboot_key, state=None, regexp="menu.opts.machine.reboot.pg_[0-9]+"),
    dp.register_callback_query_handler(menu_opts_machine_off_key, state=None, regexp="menu.opts.machine.poweroff.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_bot_key, state=None, regexp="menu.opts.bot.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_bot_off_key, state=None, regexp="menu.opts.bot.poweroff.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_bot_log_key, state=None, regexp="menu.opts.bot.log.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_access_key, state=None, regexp="menu.opts.access.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_access_minus_key, state=None, regexp="menu.opts.access.minus_id_[0-9]+.pg_[0-9]+")
    dp.register_callback_query_handler(menu_opts_access_plus_key, state=None, regexp="menu.opts.access.plus_id_[0-9]+.pg_[0-9]+")
    dp.register_callback_query_handler(menu_etc_key, state=None, regexp="menu.etc.pg_[0-9]+")
    dp.register_callback_query_handler(menu_etc_note_key, state=None, regexp="menu.etc.note.pg_[0-9]+") 
    dp.register_callback_query_handler(menu_etc_screen_key, state=None, regexp="menu.etc.screen.pg_[0-9]+")
    dp.register_callback_query_handler(menu_about, state=None, regexp="menu.about.pg_[0-9]+")
    dp.register_message_handler(menu_command, state=None, commands=['start', 'menu'])
    dp.register_message_handler(user_data, state=None, commands=['id'])