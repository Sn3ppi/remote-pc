from aiogram import Dispatcher

from models.tg.types.states.note_name.buttons import menu_key, menu_etc_key
from models.tg.types.states.note_name.messages import menu_etc_note_name_command, menu_command

def note_name_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(menu_key, state="menu.etc.note.name", regexp="menu.pg_[0-9]+")
    dp.register_callback_query_handler(menu_etc_key, state="menu.etc.note.name", regexp="menu.etc.pg_[0-9]+")
    dp.register_message_handler(menu_command, state="menu.etc.note.name", commands=['start', 'menu'])
    dp.register_message_handler(menu_etc_note_name_command, state="menu.etc.note.name",  content_types=['text'])