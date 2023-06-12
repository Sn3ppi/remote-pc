from aiogram.types import Message

from database.tables.users import get_user_data_by_outer_id, get_user_data_by_inner_id

def get_user_id_by_message_type(message: Message) -> tuple | None:
    '''Получает ID пользователя из команды, сообщения в ответ или пересланного сообщения.'''
    msg = message.text.split()
    if len(msg) == 1:
        account_type = "tg"
        if message.reply_to_message and message.reply_to_message.is_forward() and message.reply_to_message.forward_from is not None and not message.reply_to_message.forward_from.is_bot:
            user_id = message.reply_to_message.forward_from.id
        elif message.reply_to_message and not message.reply_to_message.from_user.is_bot:
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = message.from_user.id
        return get_user_data_by_outer_id(str(user_id), account_type)
    elif len(msg) == 2:
        inner_id = msg[1]
        if inner_id.isdigit():
            return get_user_data_by_inner_id(inner_id)