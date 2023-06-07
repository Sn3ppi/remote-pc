from aiogram.types import CallbackQuery, Message
from app.log import logger
from database.tables.users import get_user_level, add_user, check_last_message_id

def is_user(level: int):
    '''Проверяет уровень пользователя и принадлежность сообщения бота ему.'''
    def decorator(func):
        async def wrapper(update: CallbackQuery | Message, *args, **kwargs):
            user_id = update.from_user.id
            user_level = get_user_level(user_id, "tg")  
            if user_level is not None: 
                if user_level >= level:
                    if isinstance(update, CallbackQuery):
                        if check_last_message_id(
                            user_id=update.from_user.id, 
                            account_type="tg", 
                            last_chat_id=update.message.chat.id, 
                            last_message_id=update.message.message_id
                        ):
                            await func(update, *args, **kwargs)
                        else:
                            await update.answer()
                    else:
                        await func(update, *args, **kwargs)
                else:
                    if isinstance(update, CallbackQuery):
                        await update.answer()
            else:
                logger.info(f'Новый пользователь с ID {user_id} и типом аккаунта "tg"')
                add_user(user_id, "tg")
                if 1 >= level:
                    if isinstance(update, Message):
                        await func(update, *args, **kwargs)
                    else:
                        await update.answer()         
        return wrapper
    return decorator        