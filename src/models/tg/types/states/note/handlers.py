from aiogram import Dispatcher

from models.tg.types.states.note.buttons import *
from models.tg.types.states.note.messages import menu_etc_note_command, menu_command

def note_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(menu_key, state="menu.etc.note", regexp="menu.pg_[0-9]+")
    dp.register_callback_query_handler(menu_etc_key, state="menu.etc.note", regexp="menu.etc.pg_[0-9]+")
    dp.register_callback_query_handler(menu_etc_note_name_key, state="menu.etc.note", regexp="menu.etc.note.name.pg_[0-9]+")
    dp.register_message_handler(menu_command, state="menu.etc.note", commands=['start', 'menu'])
    dp.register_message_handler(menu_etc_note_command, state="menu.etc.note",  content_types=['text'])