import datetime
import os

from PIL import ImageGrab

from app.log import logger
from app.folders import default_note_file, custom_note_file, favorites_dir, favorites_items, screenshot_file, log_file

__all__ = [
   'pc_reboot',
   'pc_off',
   'write_note',
   'name_note',
   'delete_note',
   'screenshot',
   'get_logs',
   'start_app'
]

def pc_reboot() -> None:
    '''Перезагрузка машины.'''
    logger.info("Компьютер перезагружается.")
    os.system("cmd /k shutdown /r /t 1")


def pc_off() -> None:
    '''Выключение машины.'''
    logger.info("Компьютер выключается.")
    os.system("cmd /k shutdown /f /p")
    

def name_validation(path: str) -> str:
    '''Проверяет, соответствует ли имя файла условиям ОС.
       Проверяет, существует ли уже такой файл.
       Если проверки успешно пройдены, то возвращает изменённый полный путь для замены имени файла.'''
    repeats = 0
    
    splitted_path = os.path.splitext(os.path.basename(path))
    file_dir = os.path.dirname(path)
    user_file_name = splitted_path[0]
    default_file_name = f'{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")}'[:-3]
    file_extension = splitted_path[1]
    
    forbidden_total = ['"', ':', '|', '<', '>', '/', '\\', '?', '*']
    forbidden_begin = [' ', 'COM', 'LPT']
    forbidden_end = [' ', '.']
    forbidden_fullname = ['', 'CON', 'PRN', 'AUX', 'NUL']
    for char in forbidden_total:
        if char in user_file_name:
            user_file_name = user_file_name.replace(char, '')
    for char in forbidden_begin:
        if user_file_name.startswith(char):
            user_file_name = user_file_name[len(char):]
    for char in forbidden_end:
        if user_file_name.endswith(char):
            user_file_name = user_file_name[:-len(char)]
    if user_file_name in forbidden_fullname:
        user_file_name = default_file_name
    user_file_name = user_file_name[:255]
    
    filtered_path = os.path.join(file_dir, f"{user_file_name}{file_extension}")
    
    while os.path.exists(filtered_path):
        repeats += 1
        filtered_path = os.path.join(file_dir, f"{user_file_name}_{repeats}{file_extension}")
        
    return filtered_path


def write_note(user_id: str, text: str) -> None:
    '''Создаёт текстовый файл в папке пользователя на машине.'''
    with open(default_note_file(user_id), 'a', encoding='utf-8') as file:
        file.write(text)
        
        
def name_note(user_id: str, name: str) -> None:
    '''Даёт название текстовому файлу.'''
    default_path = default_note_file(user_id)
    new_path = name_validation(custom_note_file(user_id, name))
    os.rename(default_path, new_path)
    logger.info(f"Пользователь с ID {user_id} создал заметку по адресу {new_path}.")
       
       
def delete_note(user_id: str) -> None:
    '''Удаляет несохранённую заметку.'''
    os.remove(default_note_file(user_id))
    

def screenshot(user_id: str) -> bytes | None:
    '''Делает скриншот и сохраняет его.'''
    default_path = screenshot_file(user_id)
    new_path = name_validation(default_path)
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(new_path)
        logger.info(f"Пользователь с ID {user_id} создал скриншот по адресу {new_path}.")
        return new_path
    except OSError:
        return


def get_logs() -> str | None:
    '''Возвращает путь к лог-файлу.'''
    logs = log_file()
    if os.path.exists(logs):
        return logs
    else:
        return None


def start_app(idx: int) -> None:
    '''Открывает выбранное приложение.'''
    data = favorites_items()
    try:
        os.startfile(os.path.abspath(os.path.join(favorites_dir(), data[idx])))
    except (IndexError, FileNotFoundError):
        return