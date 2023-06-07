import re

from aiogram.types import Message, CallbackQuery, InputFile, ChatActions

from database.tables.users import set_last_message_id
from gui.keyboards.constructors import Keyboard
from models.tg.tools.keyboard_converter import KeyboardToTg

async def is_chat(update: Message | CallbackQuery) -> bool:
    '''Проверяет, групповой ли это чат.'''
    if isinstance(update, Message):
        chat_type = update.chat.type
    elif isinstance(update, CallbackQuery):
        chat_type = update.message.chat.type
    return True if chat_type in ['supergroup', 'group'] else False


async def return_message(
    update: CallbackQuery | Message,
    condition: bool=True,
    keyboard: Keyboard=None,
    text: str=None,
    document: bytes=None,
    sticker: str=None
) -> None:
    '''Возвращает различные типы контента.'''
    if sticker is not None:
        if isinstance(update, Message):
            await update.bot.send_chat_action(chat_id=update.chat.id, action=ChatActions.CHOOSE_STICKER)
            if await is_chat(update):
                await update.reply_sticker(sticker=sticker)
            else:
                await update.answer_sticker(sticker=sticker)
        elif isinstance(update, CallbackQuery):
            await update.bot.send_chat_action(chat_id=update.message.chat.id, action=ChatActions.CHOOSE_STICKER)
            await update.message.reply_sticker(sticker=sticker)
    elif document is not None:
        with open(document, 'rb') as file:
            if isinstance(update, Message):
                await update.bot.send_chat_action(chat_id=update.chat.id, action=ChatActions.UPLOAD_DOCUMENT)
                if await is_chat(update):
                    await update.reply_document(document=InputFile(file), caption=text)
                else:
                    await update.answer_document(document=InputFile(file), caption=text)
            elif isinstance(update, CallbackQuery):
                await update.bot.send_chat_action(chat_id=update.message.chat.id, action=ChatActions.UPLOAD_DOCUMENT)
                await update.message.answer_document(document=InputFile(file), caption=text)
    else:
        if isinstance(update, Message):
            await update.bot.send_chat_action(chat_id=update.chat.id, action=ChatActions.TYPING)
            if keyboard is not None:
                reply_markup = KeyboardToTg(keyboard.get_page(1))
                if await is_chat(update):
                    response = await update.reply(text=text, reply_markup=reply_markup)
                else:
                    response = await update.answer(text=text, reply_markup=reply_markup)  
                set_last_message_id(user_id=update.from_user.id, account_type="tg", last_chat_id=update.chat.id, last_message_id=response.message_id)
            else:
                await update.reply(text=text) if await is_chat(update) else await update.answer(text=text)
        elif isinstance(update, CallbackQuery):
            page = int(re.search(r'pg_(\d+)', update.data).group(1)) 
            reply_markup = KeyboardToTg(keyboard.get_page(page))
            if condition:
                await update.message.edit_text(text=text, reply_markup=reply_markup)
            else:
                await update.bot.send_chat_action(chat_id=update.message.chat.id, action=ChatActions.TYPING)
                response = await update.message.answer(text=text, reply_markup=reply_markup)
                set_last_message_id(user_id=update.from_user.id, account_type="tg", last_chat_id=update.message.chat.id, last_message_id=response.message_id)