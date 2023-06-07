import datetime
import os

from app.config.const import CACHE_DIR, BOT_DIR, DATABASE, FAVORITES_DIR, ENV_FILE, LOG_FILE

def database_file() -> str:
    '''Создаёт папку, где хранится БД.'''
    os.makedirs(BOT_DIR, exist_ok=True)
    return DATABASE


def favorites_dir() -> str:
    '''Создаёт папку, где хранятся ярлыки/ссылки на избранные программы/скрипты/папки.'''
    os.makedirs(FAVORITES_DIR, exist_ok=True)
    return FAVORITES_DIR
    
    
def favorites_items() -> list:
    '''Выводит содержимое папки с избранными приложениями в виде списка.'''
    return os.listdir(favorites_dir())

    
def get_favorites_page(start_idx: int, end_idx: int) -> list:
    '''Возвращает список избранных приложений внутри директории бота.'''
    data = list(enumerate(favorites_items()))
    return data[start_idx:end_idx+1]


def get_favorites_count() -> int:
    '''Получает количество избранных приложений.'''
    data = favorites_items()
    return len(data)
    

def config_env() -> str:
    '''Создаёт папку, где хранится .env-файл.'''
    os.makedirs(BOT_DIR, exist_ok=True)
    return ENV_FILE


def log_file() -> str:
    '''Создаёт папку, где хранится файл логов.'''
    os.makedirs(BOT_DIR, exist_ok=True)
    return LOG_FILE


def user_dir(user_id: int) -> str:
    '''Создаёт папку пользователя.'''
    path = os.path.join(CACHE_DIR, str(user_id))
    os.makedirs(path, exist_ok=True)
    return path


def screenshot_file(user_id) -> str:
    '''Возвращает путь до скриншота.'''
    return os.path.join(user_dir(user_id), f'screenshot_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")[:-3]}.png')


def default_note_file(user_id: str) -> str:
    '''Возвращает путь до заметки со стандартным названием.'''
    return os.path.join(user_dir(user_id), f'tmp_{user_id}.txt')


def custom_note_file(user_id: str, name: str) -> str:
    '''Возвращает путь до заметки с пользовательским названием.'''
    return os.path.join(user_dir(user_id), f'{name}.txt')