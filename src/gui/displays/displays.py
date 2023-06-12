'''Основное меню бота.'''

import datetime
import json

from gui.displays.constructors import Display
from utils.bytes_to_unit_name import bytes_to_unit_name
from utils.manystring import ManyString

__all__ = [
    'MenuDisplay',
    'MenuSysDisplay',
    'MenuNetDisplay',
    'MenuProgsDisplay',
    'MenuOptsDisplay',
    'MenuOptsMachineDisplay',
    'MenuOptsMachineSysDisplay',
    'MenuOptsMachineNetDisplay',
    'MenuOptsBotDisplay',
    'MenuOptsAccessDisplay',
    'MenuEtcDisplay',
    'MenuEtcNoteDisplay',
    'MenuEtcNoteNameDisplay',
    'MenuAboutDisplay'
]

class MenuDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu")
        self.set_description("ℹ️ Главное меню")
        

class MenuSysDisplay(Display):
    def __init__(self, data: str) -> None:
        super().__init__()
        self.set_header("menu.sys")
        d = ManyString()
        
        data = json.loads(data)
        last_update = None if data[0] is None else datetime.datetime.fromtimestamp(data[0])
        cpu_load = None if data[1] is None else f"{data[1]:.1f}"
        cpu_temperature = None if data[2] is None else f"{data[2]:.1f}"
        gpu_temperature = None if data[3] is None else f"{data[3]:.1f}"
        disks = None if data[4] is None else json.loads(data[4])
        free_ram = None if data[5] is None else bytes_to_unit_name(data[5])
        total_ram = None if data[6] is None else bytes_to_unit_name(data[6])
        percent_ram = None if data[7] is None else f"{data[7]:.2f}"
        uptime = None if data[8] is None else datetime.timedelta(seconds=int(f"{data[8]:.0f}"))
        
        d.enter(f"🕑 Последнее обновление (системное время):")
        d.enter(f"{last_update}")
        d.enter(f"🌡 Температура:", space=2)
        d.enter(f"CPU: {cpu_temperature} °C")
        d.enter(f"GPU: {gpu_temperature} °C")
        d.enter(f"🏎 Загрузка процессора: {cpu_load} %", space=2)
        
        if disks is not None:
            d.enter(f"📀 Объём свободной памяти на смонтированных разделах:", space=2)
            for disk in disks:
                dev_name = disk
                free_mem = bytes_to_unit_name(disks[disk]["free"])
                total_mem = bytes_to_unit_name(disks[disk]["total"])
                percent_mem = f'{disks[disk]["percent"]:.2f}'
                d.enter(f'{dev_name} {free_mem} / {total_mem} ({percent_mem} %)')
            
        d.enter(f"RAM: {free_ram} / {total_ram} ({percent_ram} %)", space=2)
        d.enter(f"⏳ UPTIME: {uptime}", space=2)
        self.set_description(str(d))
        
        
class MenuNetDisplay(Display):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.set_header("menu.net")
        d = ManyString()
        
        data = json.loads(data)
        last_update = None if data[0] is None else datetime.datetime.fromtimestamp(data[0])
        download_speed = None if data[1] is None else bytes_to_unit_name(data[1])
        upload_speed = None if data[2] is None else bytes_to_unit_name(data[2])
    
        d.enter(f"Последнее обновление (системное время):")
        d.enter(f"{last_update}")
        d.enter(f"⬆️ Скорость загрузки: {download_speed}", space=2)
        d.enter(f"⬇️ Скорость отправки: {upload_speed}")
        self.set_description(str(d))
        
        
class MenuProgsDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.progs")
        self.set_description("ℹ️ Быстрый доступ к папкам и программам.")
        

class MenuOptsDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.opts")
        self.set_description("ℹ️ Выберите, что хотите настроить:")
        
        
class MenuOptsMachineDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.opts.machine")
        self.set_description("ℹ️ Настройки компьютера.")
        
        
class MenuOptsMachineSysDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.opts.machine.sys")
        self.set_description("ℹ️ Настройки частоты обновления данных о системе.")
        

class MenuOptsMachineNetDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.opts.machine.net")
        self.set_description("ℹ️ Настройки частоты обновления данных об Интернет-соединении.")
        

class MenuOptsBotDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.opts.bot")
        d = ManyString()
        d.enter("ℹ️ Настройки бота.")
        self.set_description(str(d))

        
class MenuOptsAccessDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.opts.access")
        d = ManyString()
        d.enter("ℹ️ Настройки привилегий зарегистрированных пользователей:")
        d.enter("ℹ️ Уровень 0: пользователь игнорируется.")
        d.enter("ℹ️ Уровень 1: пользователь может только просматривать информацию о компьютере.")
        d.enter("ℹ️ Уровень 2: пользователь может оставлять заметки, а также получать информацию о пользователях командой /id.")
        d.enter("ℹ️ /id - возвращает ID отправившего команду пользователя, ID пользователя из сообщения или ID пользователя в мессенджере по внутреннему ID.")
        d.enter("ℹ️ Уровень 3: у пользователя есть полный доступ к настройкам бота, но он не получает уведомлений о запуске.")
        d.enter("ℹ️ Уровень 4: у пользователя есть полный доступ к настройкам бота, а также он получает уведомления о запуске.")
        self.set_description(str(d))
        
        
class MenuEtcDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.etc")
        self.set_description("ℹ️ Выберите одно из действий:")
        
        
class MenuEtcNoteDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.etc.note")
        d = ManyString()
        d.enter("[1/2] Напишите заметку.")
        d.enter('ℹ️ Когда завершите написание заметки, нажмите "🆗 Продолжить".')
        self.set_description(str(d))
        
        
class MenuEtcNoteNameDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.etc.note.name")
        d = ManyString()
        d.enter("[2/2] Назовите заметку.")
        d.enter('Нажмите "Назад", если Вы не хотите сохранять заметку.')
        self.set_description(str(d))
        
        
class MenuAboutDisplay(Display):
    def __init__(self) -> None:
        super().__init__()
        self.set_header("menu.about")
        self.set_description("ℹ️ Авторы проекта.")