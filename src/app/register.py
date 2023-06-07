import dotenv

from app.folders import config_env
from app.log import logger

def reset_tg_bot_token() -> None:
    '''Сбрасывает токен бота Telegram в Telegram.'''
    dotenv.set_key(config_env(), "TG_BOT_TOKEN", "")
    logger.warning("Токен Telegram-бота был сброшен, т.к. при его написании допущена синтаксическая ошибка.")
    
    
def reset_tg_admin_id() -> None:
    '''Сбрасывает ID владельца машины  в Telegram.'''
    dotenv.set_key(config_env(), "TG_ADMIN_ID", "")
    logger.warning("ID администратора в Telegram был сброшен, т.к. при его написании допущена синтаксическая ошибка.")
    
    
def get_tg_admin_id() -> str:
    '''Получает ID владельца машины в Telegram.'''
    result = dotenv.get_key(config_env(), "TG_ADMIN_ID")
    return "" if result is None else result


def get_tg_bot_token() -> str:
    '''Получает ID владельца машины в Telegram.'''
    result = dotenv.get_key(config_env(), "TG_BOT_TOKEN")
    return "" if result is None else result
    
    
def default_env() -> None:
    '''Создаёт .env-файл с нулевыми значениями, если он не существует.'''
    with open(config_env(), 'w') as file:
        file.truncate(0)
    reset_tg_bot_token()
    reset_tg_admin_id()
    
    
def validate_keys() -> None:
    '''Читает .env-файл и проверяет поля.
       Сбрасывает значения полей.'''
    valid_keys = ['TG_BOT_TOKEN', 'TG_ADMIN_ID']
    env_keys = list(dotenv.dotenv_values(config_env()))
    if env_keys != valid_keys:
        default_env()