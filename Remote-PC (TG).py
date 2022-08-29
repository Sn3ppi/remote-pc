import sys

from remote_pc.bot_parts import stats
from remote_pc.bot_parts import machine
from remote_pc.bot_parts import settings
from remote_pc.bot_parts import display

from remote_pc.tg_parts import keyboard as key
from remote_pc.tg_parts import gen
from remote_pc.tg_parts import classes

import re
import logging
import asyncio 
import sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions
from asyncio import set_event_loop, new_event_loop
import json

logging.basicConfig(level=logging.INFO)
bot = Bot(settings.json_config_parse()["bot_options"]["token"], parse_mode="HTML") 
dp = Dispatcher(bot, storage=MemoryStorage())

async def on_boot():
    config = settings.json_config_parse()
    stats.info_auto_update()
    await stats.log("Бот запущен!")
    users = config["permissions"]["notify"]
    for user in users:
        if str(user) in config["permissions"]["notify"]:
            try:
                await bot.send_message(user, text="ℹ️ Бот запущен!", reply_markup=key.main_menu())
            except Exception as e:
                await stats.log(f"{user}: {e}")
                continue

@dp.errors_handler(exception=exceptions.BotBlocked)
async def bot_blocked(update: types.Update, exception: exceptions.BotBlocked):
    await bot.send_message(update.callback_query.message.chat.id, f"Вы заблокировали бота! Не могу отправить сообщение...", reply_markup=key.private())
    return True

@dp.errors_handler(exception=exceptions.CantInitiateConversation)
async def cant_initiate_conversation(update: types.Update, exception: exceptions.CantInitiateConversation):
    await bot.send_message(update.callback_query.message.chat.id, f"Сначала начните диалог со мной! Не могу отправить сообщение...", reply_markup=key.private())
    return True

@dp.errors_handler(exception=exceptions.MessageNotModified)
async def message_not_modified(update: types.Update, exception: exceptions.CantInitiateConversation):
    return True

@dp.errors_handler(exception=exceptions.RetryAfter)
async def flood_wait_retry_after(update: types.Update, exception: exceptions.RetryAfter):
    await stats.log(f"Подозрительная активность! Попробуйте через {exception.timeout} с.")
    await asyncio.sleep(exception.timeout)
    return True

@dp.callback_query_handler(state=classes.main_menu, text=json.dumps({"type": "bot_menu", "act": "check"})) 
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.main_menu()}", reply_markup=key.main_menu())
    await state.finish()

@dp.callback_query_handler(state=classes.notes, text=json.dumps({"type": "bot_menu", "act": "check"}))
async def note_delete(call: types.CallbackQuery, state: FSMContext): 
    await machine.delete_path(f'{call.from_user.id}/tmp_{call.from_user.id}.txt')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.main_menu()}", reply_markup=key.main_menu())
    await state.finish()

@dp.message_handler(state=classes.main_menu, commands=['start', 'help'])
async def main_menu(message: types.Message, state: FSMContext):
    await gen.return_message(message, text=f"{await display.main_menu()}", reply_markup=key.main_menu())
    await state.finish()

@dp.message_handler(state=classes.notes, commands=['start','help'])
async def note_delete(message: types.Message, state: FSMContext):
    await machine.delete_path(f'{message.from_user.id}/tmp_{message.from_user.id}.txt')
    await gen.return_message(message, text=f"{await display.main_menu()}", reply_markup=key.main_menu())
    await state.finish()

@dp.callback_query_handler(state=classes.main_menu + classes.notes, text=json.dumps({"type": "bot_menu", "act": "delete"}))
async def close_window(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()

@dp.message_handler(text=[f'@{settings.get_bot_username()}'])
async def sneppi(message: types.Message):  
    await gen.return_message(message, sticker="CAACAgIAAxkBAAEKmttg276yQK1rvsQSBM80_Eyc0gt2DAACCQADci8wB6PyDmoZHBAlIAQ")

@dp.callback_query_handler(text=json.dumps({"type": "sys_menu", "act": "check"}))
async def sys_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "sys_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_menu()}", reply_markup=key.sys_menu())

@dp.callback_query_handler(text=json.dumps({"type": "sys_menu", "act": "upd"}))
async def sys_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "sys_menu", "upd"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Обновляю данные...")
        await stats.manual_sys_update()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_menu()}", reply_markup=key.sys_menu())

@dp.callback_query_handler(text=json.dumps({"type": "net_menu", "act": "check"})) 
async def net_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "net_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_menu()}", reply_markup=key.net_menu())

@dp.callback_query_handler(text=json.dumps({"type": "net_menu", "act": "upd"}))
async def net_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "net_menu", "upd"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Обновляю данные...")
        await stats.manual_net_update()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_menu()}", reply_markup=key.net_menu())

@dp.callback_query_handler(text=json.dumps({"type": "progs_menu", "act": "check"}))
async def progs_menu(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_menu()}", reply_markup=key.progs_menu())

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "progs_menu", "act": "list"}))
async def progs_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_open()}", reply_markup=key.dynamic_keyboard("progs_menu", "progs", "open", count=0, step=5))

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "progs_menu", "act": "list"}))
async def progs_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.send_message(call.from_user.id, text=f"{await display.progs_open()}", reply_markup=key.dynamic_keyboard("progs_menu", "progs", "open", count=0, step=5))
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_menu", "act": "open", "page": "[0-9]+"})) 
async def progs_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        page = json.loads(call.data)["page"] 
        await call.message.edit_text(text=f"{await display.progs_open()}", reply_markup=key.dynamic_keyboard("progs_menu", "progs", "open", count=int(page), step=5))

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_menu", "act": "open", "id": "[0-9]+"})) 
async def progs_open(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        await settings.progs_open(json.loads(call.data)["id"])

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "progs_menu", "act": "add"}))
async def progs_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_add()}", reply_markup=key.progs_add())
        await classes.Progs.add_path.set()

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "progs_menu", "act": "add"}))
async def progs_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.send_message(call.from_user.id, text=f"{await display.progs_add()}", reply_markup=key.progs_add())
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())
        state = dp.current_state(chat=call.from_user.id, user=call.from_user.id)
        await state.set_state(classes.Progs.add_path)

@dp.callback_query_handler(state=classes.Progs.add_path, text=json.dumps({"type": "progs_menu", "act": "check"}))
async def progs_add_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_menu()}", reply_markup=key.progs_menu())
        await state.finish()

@dp.message_handler(state=classes.Progs.add_path, content_types=['text'])
async def progs_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "progs_menu"):
        if await settings.progs_add(message.text):
            await gen.return_message(message, text=f"{await display.progs_menu()}", reply_markup=key.progs_menu())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.progs_err()}", reply_markup=key.progs_add())

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "progs_menu", "act": "delete_0"}))
async def progs_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_delete()}", reply_markup=key.dynamic_keyboard("progs_menu", "progs", "delete"))

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "progs_menu", "act": "delete_0"}))
async def progs_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        await bot.send_message(call.from_user.id, text=f"{await display.progs_delete()}", reply_markup=key.dynamic_keyboard("progs_menu", "progs", "delete"))
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_menu", "act": "delete", "page": "[0-9]+"})) 
async def progs_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_delete()}", reply_markup=key.dynamic_keyboard("progs_menu", "progs", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_menu", "act": "delete", "id": "[0-9]+"}))  
async def  progs_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "progs_menu"):
        await settings.progs_remove(json.loads(call.data)["id"])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_menu()}", reply_markup=key.progs_menu())

@dp.callback_query_handler(text=json.dumps({"type": "etc_menu", "act": "check"}))
async def etc_menu(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.etc_menu()}", reply_markup=key.etc_menu())

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "screen_menu", "act": "take"}))
async def screen_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "screen_menu"):
        file = await machine.screenshot(f"{call.from_user.id}")
        if file == False:
            await bot.send_message(call.from_user.id, text=f"{await display.screen_err()}", reply_markup=key.screen_menu())
        await bot.send_document(call.from_user.id, open(file, 'rb'))
        await bot.send_message(call.from_user.id, text=f"{await display.screen_menu()}", reply_markup=key.screen_menu())
        
@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "screen_menu", "act": "take"}))
async def screen_menu(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "screen_menu"):
        file = await machine.screenshot(f"{call.from_user.id}")
        if file == False:
            await bot.send_message(call.from_user.id, text=f"{await display.screen_err()}", reply_markup=key.screen_menu())
        await bot.send_document(call.from_user.id, open(file, 'rb'))
        await bot.send_message(call.from_user.id, text=f"{await display.screen_menu()}", reply_markup=key.screen_menu())
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "note_menu", "act": "write"}))
async def note_menu_0(call: types.CallbackQuery, state: FSMContext): 
    if await gen.is_user(call, call.message, "note_menu"):
        await bot.send_message(call.from_user.id, text=f"{await display.note_menu_0()}", reply_markup=key.note_menu_0())
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())
        state = dp.current_state(chat=call.from_user.id, user=call.from_user.id)
        await state.set_state(classes.Note.menu_1)

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "note_menu", "act": "write"}))
async def note_menu_0(call: types.CallbackQuery, state: FSMContext): 
    if await gen.is_user(call, call.message, "note_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_menu_0()}", reply_markup=key.note_menu_0())
        await classes.Note.menu_1.set()

@dp.message_handler(state=classes.Note.menu_1, content_types=['text']) 
async def note_menu_1(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "note_menu"):
        if await machine.write_note(message.from_user.id, message.text):
            await gen.return_message(message, text=f"{await display.note_menu_1()}", reply_markup=key.note_menu_1())
        else:
            await gen.return_message(message, text=f"{await display.note_err()}", reply_markup=key.note_menu_1())

@dp.callback_query_handler(state=classes.Note.menu_1, text=json.dumps({"type": "note_menu", "act": "done"})) 
async def note_menu_1(call: types.CallbackQuery, state: FSMContext): 
    if await gen.is_user(call, call.message, "note_menu"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_menu_2()}", reply_markup=key.note_menu_2())
        await classes.Note.menu_2.set()

@dp.message_handler(state=classes.Note.menu_2, content_types=['text']) 
async def note_menu_2(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "note_menu"):
        if await machine.name_note(message.from_user.id, message.text):
            await gen.return_message(message, text=f"{await display.main_menu()}", reply_markup=key.main_menu())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.note_err()}", reply_markup=key.note_menu_2())

@dp.callback_query_handler(state=classes.notes, text=json.dumps({"type": "note_menu", "act": "delete"}))
async def note_delete(call: types.CallbackQuery, state: FSMContext): 
    if await gen.is_user(call, call.message, "note_menu"):
        await machine.delete_path(f'{call.from_user.id}/tmp_{call.from_user.id}.txt')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.etc_menu()}", reply_markup=key.etc_menu())
        await state.finish()

@dp.callback_query_handler(state=classes.notes, text=json.dumps({"type": "etc_menu", "act": "check"}))
async def note_delete(call: types.CallbackQuery, state: FSMContext):
    await machine.delete_path(f'{call.from_user.id}/tmp_{call.from_user.id}.txt')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.etc_menu()}", reply_markup=key.etc_menu())
    await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "opts", "act": "check"}))
async def opts(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.opts()}", reply_markup=key.opts())

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "machine_opts", "act": "check"}))
async def machine_opts(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "machine_opts"):
        await bot.send_message(call.from_user.id, text=f"{await display.machine_opts()}", reply_markup=key.machine_opts())
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "machine_opts", "act": "check"}))
async def machine_opts(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "machine_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_opts()}", reply_markup=key.machine_opts())

@dp.callback_query_handler(state=[classes.SysOpts.edit, classes.NetOpts.edit], text=json.dumps({"type": "machine_opts", "act": "check"}))
async def machine_opts_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "machine_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_opts()}", reply_markup=key.machine_opts())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "machine_opts", "act": "sys"}))
async def sys_opts_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "machine_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_opts()}", reply_markup=key.machine_act())
        await classes.SysOpts.edit.set()

@dp.message_handler(state=classes.SysOpts.edit, content_types=['text'])
async def sys_opts_edit(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "machine_opts"):
        if await settings.set_sys_autoupdate_frequency(message.text):
            await gen.return_message(message, text=f"{await display.machine_opts()}", reply_markup=key.machine_opts())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.sys_opts()}", reply_markup=key.machine_act())

@dp.callback_query_handler(text=json.dumps({"type": "machine_opts", "act": "net"}))
async def net_opts_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "machine_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_opts()}", reply_markup=key.machine_act())
        await classes.NetOpts.edit.set()

@dp.message_handler(state=classes.NetOpts.edit, content_types=['text'])
async def net_opts_edit(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "machine_opts"):
        if await settings.set_net_autoupdate_frequency(message.text):
            await gen.return_message(message, text=f"{await display.machine_opts()}", reply_markup=key.machine_opts())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.net_opts()}", reply_markup=key.machine_act())

@dp.callback_query_handler(text=json.dumps({"type": "machine_opts", "act": "reload"}))
async def machine_reload(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "machine_opts"):
        await machine.reload(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_reload(call.from_user.id)}")

@dp.callback_query_handler(text=json.dumps({"type": "machine_opts", "act": "off"}))
async def machine_off(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "machine_opts"):
        await machine.poweroff(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_off(call.from_user.id)}")

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "bot_opts", "act": "check"}))
async def bot_opts(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "bot_opts"):
        await bot.send_message(call.from_user.id, text=f"{await display.bot_opts()}", reply_markup=key.bot_opts())
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "bot_opts", "act": "check"}))
async def bot_opts(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "bot_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_opts()}", reply_markup=key.bot_opts())

@dp.callback_query_handler(text=json.dumps({"type": "bot_opts", "act": "log"}))
async def set_logs_status(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "bot_opts"):
        await settings.set_logs_status()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_opts()}", reply_markup=key.bot_opts())

@dp.callback_query_handler(text=json.dumps({"type": "bot_opts", "act": "off"}))
async def set_logs_status(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "bot_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_off(call.from_user.id)}")
        await machine.bot_off(call.from_user.id)

@dp.callback_query_handler(chat_type=["group", "supergroup"], text=json.dumps({"type": "access_opts", "act": "check"}))
async def access_opts(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.send_message(call.from_user.id, text=f"{await display.access_opts()}", reply_markup=key.access_opts())
        await gen.return_message(call.message, text=f"{await display.private()}", reply_markup=key.private())

@dp.callback_query_handler(chat_type="private", text=json.dumps({"type": "access_opts", "act": "check"}))
async def access_opts(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
       await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_opts()}", reply_markup=key.access_opts())

@dp.callback_query_handler(text=json.dumps({"type": "sys_perm", "act": "check"}))
async def sys_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm()}", reply_markup=key.sys_perm())

@dp.callback_query_handler(state=classes.SysPerm.add, text=json.dumps({"type": "sys_perm", "act": "check"}))
async def sys_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm()}", reply_markup=key.sys_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "sys_perm", "act": "info"}))
async def set_sys_status(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await settings.set_sysinfo_privacy()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm()}", reply_markup=key.sys_perm())

@dp.callback_query_handler(text=json.dumps({"type": "sys_perm", "act": "add"})) 
async def sys_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm_add()}", reply_markup=key.sys_perm_add())
        await classes.SysPerm.add.set()

@dp.message_handler(state=classes.SysPerm.add, content_types=['text'])
async def sys_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "sys_menu", "add"):
            await gen.return_message(message, text=f"{await display.sys_perm()}", reply_markup=key.sys_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.sys_perm_add()}", reply_markup=key.sys_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "sys_perm", "act": "delete_0"})) 
async def sys_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm_delete()}", reply_markup=key.dynamic_keyboard("sys_perm", "sys_menu", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "sys_perm", "act": "delete", "page": "[0-9]+"})) 
async def sys_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm_delete()}", reply_markup=key.dynamic_keyboard("sys_perm", "sys_menu", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "sys_perm", "act": "delete", "id": "[0-9]+"}))  
async def sys_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "sys_menu", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.sys_perm()}", reply_markup=key.sys_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "net_perm", "act": "check"}))
async def net_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm()}", reply_markup=key.net_perm())

@dp.callback_query_handler(state=classes.NetPerm.add, text=json.dumps({"type": "net_perm", "act": "check"}))
async def net_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm()}", reply_markup=key.net_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "net_perm", "act": "info"}))
async def set_net_status(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await settings.set_netinfo_privacy()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm()}", reply_markup=key.net_perm())

@dp.callback_query_handler(text=json.dumps({"type": "net_perm", "act": "add"})) 
async def net_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm_add()}", reply_markup=key.net_perm_add())
        await classes.NetPerm.add.set()

@dp.message_handler(state=classes.NetPerm.add, content_types=['text'])
async def net_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "net_menu", "add"):
            await gen.return_message(message, text=f"{await display.net_perm()}", reply_markup=key.net_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.net_perm_add()}", reply_markup=key.net_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "net_perm", "act": "delete_0"})) 
async def net_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm_delete()}", reply_markup=key.dynamic_keyboard("net_perm", "net_menu", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "net_perm", "act": "delete", "page": "[0-9]+"})) 
async def net_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm_delete()}", reply_markup=key.dynamic_keyboard("net_perm", "net_menu", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "net_perm", "act": "delete", "id": "[0-9]+"}))  
async def net_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "net_menu", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.net_perm()}", reply_markup=key.net_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "progs_perm", "act": "check"}))
async def progs_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_perm()}", reply_markup=key.progs_perm())
####
@dp.callback_query_handler(state=classes.ProgsPerm.add, text=json.dumps({"type": "progs_perm", "act": "check"}))
async def progs_perm(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_perm()}", reply_markup=key.progs_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "progs_perm", "act": "add"})) 
async def progs_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_perm_add()}", reply_markup=key.progs_perm_add())
        await classes.ProgsPerm.add.set()

@dp.message_handler(state=classes.ProgsPerm.add, content_types=['text'])
async def progs_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "progs_menu", "add"):
            await gen.return_message(message, text=f"{await display.progs_perm()}", reply_markup=key.progs_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.progs_perm_add()}", reply_markup=key.progs_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_perm", "act": "delete_0"})) 
async def progs_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_perm_delete()}", reply_markup=key.dynamic_keyboard("progs_perm", "progs_menu", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_perm", "act": "delete", "page": "[0-9]+"})) 
async def progs_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_perm_delete()}", reply_markup=key.dynamic_keyboard("progs_perm", "progs_menu", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "progs_perm", "act": "delete", "id": "[0-9]+"}))  
async def progs_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "progs_menu", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.progs_perm()}", reply_markup=key.progs_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "screen_perm", "act": "check"}))
async def screen_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.screen_perm()}", reply_markup=key.screen_perm())

@dp.callback_query_handler(state=classes.ScreenPerm.add, text=json.dumps({"type": "screen_perm", "act": "check"}))
async def screen_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.screen_perm()}", reply_markup=key.screen_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "screen_perm", "act": "add"})) 
async def screen_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.screen_perm_add()}", reply_markup=key.screen_perm_add())
        await classes.ScreenPerm.add.set()

@dp.message_handler(state=classes.ScreenPerm.add, content_types=['text'])
async def screen_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "screen_menu", "add"):
            await gen.return_message(message, text=f"{await display.screen_perm()}", reply_markup=key.screen_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.screen_perm_add()}", reply_markup=key.screen_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "screen_perm", "act": "delete_0"})) 
async def screen_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.screen_perm_delete()}", reply_markup=key.dynamic_keyboard("screen_perm", "screen_menu", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "screen_perm", "act": "delete", "page": "[0-9]+"})) 
async def screen_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.screen_perm_delete()}", reply_markup=key.dynamic_keyboard("screen_perm", "screen_menu", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "screen_perm", "act": "delete", "id": "[0-9]+"}))  
async def screen_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "screen_menu", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.screen_perm()}", reply_markup=key.screen_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "note_perm", "act": "check"}))
async def note_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_perm()}", reply_markup=key.note_perm())

@dp.callback_query_handler(state=classes.NotePerm.add, text=json.dumps({"type": "note_perm", "act": "check"}))
async def note_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_perm()}", reply_markup=key.note_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "note_perm", "act": "add"})) 
async def note_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_perm_add()}", reply_markup=key.note_perm_add())
        await classes.NotePerm.add.set()

@dp.message_handler(state=classes.NotePerm.add, content_types=['text'])
async def note_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "note_menu", "add"):
            await gen.return_message(message, text=f"{await display.note_perm()}", reply_markup=key.note_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.note_perm_add()}", reply_markup=key.note_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "note_perm", "act": "delete_0"})) 
async def note_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_perm_delete()}", reply_markup=key.dynamic_keyboard("note_perm", "note_menu", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "note_perm", "act": "delete", "page": "[0-9]+"})) 
async def note_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_perm_delete()}", reply_markup=key.dynamic_keyboard("note_perm", "note_menu", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "note_perm", "act": "delete", "id": "[0-9]+"}))  
async def note_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "note_menu", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.note_perm()}", reply_markup=key.note_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "machine_perm", "act": "check"}))
async def machine_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_perm()}", reply_markup=key.machine_perm())

@dp.callback_query_handler(state=classes.MachinePerm.add, text=json.dumps({"type": "machine_perm", "act": "check"}))
async def machine_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_perm()}", reply_markup=key.machine_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "machine_perm", "act": "add"})) 
async def machine_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_perm_add()}", reply_markup=key.machine_perm_add())
        await classes.MachinePerm.add.set()

@dp.message_handler(state=classes.MachinePerm.add, content_types=['text'])
async def machine_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "machine_opts", "add"):
            await gen.return_message(message, text=f"{await display.machine_perm()}", reply_markup=key.machine_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.machine_perm_add()}", reply_markup=key.machine_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "machine_perm", "act": "delete_0"})) 
async def machine_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_perm_delete()}", reply_markup=key.dynamic_keyboard("machine_perm", "machine_opts", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "machine_perm", "act": "delete", "page": "[0-9]+"})) 
async def machine_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_perm_delete()}", reply_markup=key.dynamic_keyboard("machine_perm", "machine_opts", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "machine_perm", "act": "delete", "id": "[0-9]+"}))  
async def machine_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "machine_opts", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.machine_perm()}", reply_markup=key.machine_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "notify_perm", "act": "check"}))
async def notify_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.notify_perm()}", reply_markup=key.notify_perm())

@dp.callback_query_handler(state=classes.OnBootNotifyPerm.add, text=json.dumps({"type": "notify_perm", "act": "check"}))
async def notify_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.notify_perm()}", reply_markup=key.notify_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "notify_perm", "act": "add"})) 
async def notify_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.notify_perm_add()}", reply_markup=key.notify_perm_add())
        await classes.OnBootNotifyPerm.add.set()

@dp.message_handler(state=classes.OnBootNotifyPerm.add, content_types=['text'])
async def notify_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "notify", "add"):
            await gen.return_message(message, text=f"{await display.notify_perm()}", reply_markup=key.notify_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.notify_perm_add()}", reply_markup=key.notify_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "notify_perm", "act": "delete_0"})) 
async def notify_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.notify_perm_delete()}", reply_markup=key.dynamic_keyboard("notify_perm", "notify", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "notify_perm", "act": "delete", "page": "[0-9]+"})) 
async def notify_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.notify_perm_delete()}", reply_markup=key.dynamic_keyboard("notify_perm", "notify", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "notify_perm", "act": "delete", "id": "[0-9]+"}))  
async def notify_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "notify", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.notify_perm()}", reply_markup=key.notify_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "bot_perm", "act": "check"}))
async def bot_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_perm()}", reply_markup=key.bot_perm())

@dp.callback_query_handler(state=classes.BotPerm.add, text=json.dumps({"type": "bot_perm", "act": "check"})) 
async def bot_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_perm()}", reply_markup=key.bot_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "bot_perm", "act": "add"})) 
async def bot_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_perm_add()}", reply_markup=key.bot_perm_add())
        await classes.BotPerm.add.set()

@dp.message_handler(state=classes.BotPerm.add, content_types=['text'])
async def bot_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "bot_opts", "add"):
            await gen.return_message(message, text=f"{await display.bot_perm()}", reply_markup=key.bot_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.bot_perm_add()}", reply_markup=key.bot_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "bot_perm", "act": "delete_0"})) 
async def bot_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_perm_delete()}", reply_markup=key.dynamic_keyboard("bot_perm", "bot_opts", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "bot_perm", "act": "delete", "page": "[0-9]+"})) 
async def bot_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_perm_delete()}", reply_markup=key.dynamic_keyboard("bot_perm", "bot_opts", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "bot_perm", "act": "delete", "id": "[0-9]+"}))  
async def bot_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "bot_opts", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.bot_perm()}", reply_markup=key.bot_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(text=json.dumps({"type": "access_perm", "act": "check"}))
async def access_perm(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_perm()}", reply_markup=key.access_perm())

@dp.callback_query_handler(state=classes.AccessPerm.add, text=json.dumps({"type": "access_perm", "act": "check"}))
async def access_perm_b(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_perm()}", reply_markup=key.access_perm())
        await state.finish()

@dp.callback_query_handler(text=json.dumps({"type": "access_perm", "act": "add"})) 
async def access_perm_add_0(call: types.CallbackQuery, state: FSMContext):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_perm_add()}", reply_markup=key.access_perm_add())
        await classes.AccessPerm.add.set()

@dp.message_handler(state=classes.AccessPerm.add, content_types=['text'])
async def access_perm_add(message: types.Message, state: FSMContext):
    if await gen.is_user(message, message, "access_opts"):
        if await settings.change_users(message.from_user.id, message.text, "access_opts", "add"):
            await gen.return_message(message, text=f"{await display.access_perm()}", reply_markup=key.access_perm())
            await state.finish()
        else:
            await gen.return_message(message, text=f"{await display.access_perm_add()}", reply_markup=key.access_perm_add())

@dp.callback_query_handler(regexp=json.dumps({"type": "access_perm", "act": "delete_0"})) 
async def access_perm_delete_0(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_perm_delete()}", reply_markup=key.dynamic_keyboard("access_perm", "access_opts", act="delete"))

@dp.callback_query_handler(regexp=json.dumps({"type": "access_perm", "act": "delete", "page": "[0-9]+"})) 
async def access_perm_delete_page(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        page = json.loads(call.data)["page"] 
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_perm_delete()}", reply_markup=key.dynamic_keyboard("access_perm", "access_opts", act="delete", count=int(page)))

@dp.callback_query_handler(regexp=json.dumps({"type": "access_perm", "act": "delete", "id": "[0-9]+"}))  
async def access_perm_delete_act(call: types.CallbackQuery):
    if await gen.is_user(call, call.message, "access_opts"):
        user = json.loads(call.data)["id"]
        if await settings.change_users(call.from_user.id, user, "access_opts", "delete"):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.access_perm()}", reply_markup=key.access_perm())
        else:
            await gen.return_message(call.message, text="⚠️ Вы не можете удалить разрешение у самого себя.")

@dp.callback_query_handler(regexp=json.dumps({"type": "config_opts", "act": "delete_0"})) 
async def config_delete_0(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{await display.config_opts()}", reply_markup=key.config_opts())

@dp.callback_query_handler(regexp=json.dumps({"type": "config_opts", "act": "delete"})) 
async def config_delete(call: types.CallbackQuery):
    config = settings.json_config_parse()
    await stats.log("Настройки бота сброшены! Перезапустите бота после настройки.")
    users = config["permissions"]["notify"]
    for user in users:
        if str(user) in config["permissions"]["notify"]:
            try:
                await bot.send_message(user, text="ℹ️ Настройки бота сброшены!\nПерезапустите бота после настройки.")
            except Exception as e:
                await stats.log(f"{user}: {e}")
                continue
    dp.stop_polling()
    settings.json_config_delete()
    await settings.register()
   

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(on_boot())
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        pass