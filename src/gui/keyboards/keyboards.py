from gui.keyboards.constructors import Button, Row, Keyboard
from gui.keyboards.templates import UserRow, ProgrammRow

__all__ = [
    'MenuKeyboard',
    'MenuSysKeyboard',
    'MenuNetKeyboard',
    'MenuProgsKeyboard',
    'MenuOptsKeyboard',
    'MenuOptsMachineKeyboard',
    'MenuOptsMachineSysKeyboard',
    'MenuOptsMachineNetKeyboard',
    'MenuOptsBotKeyboard',
    'MenuOptsAccessKeyboard',
    'MenuEtcKeyboard',
    'MenuEtcNoteKeyboard',
    'MenuEtcNoteNameKeyboard',
    'MenuAboutKeyboard'
]

class MenuKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 1
        self.current_menu = "menu"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="🖥 Система", callback_data="menu.sys.pg_1")),
            Row(Button(text="🌐 Интернет", callback_data="menu.net.pg_1")),
            Row(Button(text="🕹 Программы", callback_data="menu.progs.pg_1")),
            Row(Button(text="⚙️ Настройки", callback_data="menu.opts.pg_1")),
            Row(Button(text="➡️ Ещё...", callback_data="menu.etc.pg_1")),
            Row(Button(text="ℹ️ Авторы", callback_data="menu.about.pg_1"))
        ])
        
        
class MenuSysKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 2
        self.home_menu = "menu"
        self.current_menu = "menu.sys"
        self.previous_menu = "menu"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="🔄 Обновить", callback_data="menu.sys.pg_1"))
        ])
        
        
class MenuNetKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 2
        self.home_menu = "menu"
        self.current_menu = "menu.net"
        self.previous_menu = "menu"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="🔄 Обновить", callback_data="menu.net.pg_1"))
        ])
        
        
class MenuProgsKeyboard(Keyboard):
    def __init__(self, generator, count: int) -> None:
        super().__init__()
        self.depth = 2
        self.home_menu = "menu"
        self.current_menu = "menu.progs"
        self.previous_menu = "menu"
        self.rows_per_page = 5
        self.add_dynamic_items(
            generator,
            ProgrammRow,
            count
        )
        

class MenuOptsKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 2
        self.home_menu = "menu"
        self.current_menu = "menu.opts"
        self.previous_menu = "menu"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="🖥 Компьютер", callback_data="menu.opts.machine.pg_1")),
            Row(Button(text="🤖 Бот", callback_data="menu.opts.bot.pg_1")),
            Row(Button(text="👤 Привилегии", callback_data="menu.opts.access.pg_1"))
        ])
        
        
class MenuOptsMachineKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 3
        self.home_menu = "menu"
        self.current_menu = "menu.opts.machine"
        self.previous_menu = "menu.opts"
        self.rows_per_page = 5  
        self.add_static_items([
            Row(Button(text="🖥 Система", callback_data="menu.opts.machine.sys.pg_1")),
            Row(Button(text="🌐 Интернет", callback_data="menu.opts.machine.net.pg_1")),
            Row(Button(text="🔄 Перезагрузить", callback_data="menu.opts.machine.reboot")),
            Row(Button(text="❌ Выключить", callback_data="menu.opts.machine.poweroff"))
        ])
        
        
class MenuOptsMachineSysKeyboard(Keyboard):
    def __init__(self, frequency: int) -> None:
        super().__init__()
        self.depth = 4
        self.home_menu = "menu"
        self.current_menu = "menu.opts.machine.sys"
        self.previous_menu = "menu.opts.machine"
        self.rows_per_page = 5
        self.add_static_items([
            Row(
                Button(text="-", callback_data="menu.opts.machine.sys.minus"),
                Button(text=f"{frequency}"),
                Button(text="+", callback_data="menu.opts.machine.sys.plus")
            )
        ])
        
        
class MenuOptsMachineNetKeyboard(Keyboard):
    def __init__(self, frequency: int) -> None:
        super().__init__()
        self.depth = 4
        self.home_menu = "menu"
        self.current_menu = "menu.opts.machine.net"
        self.previous_menu = "menu.opts.machine"
        self.rows_per_page = 5
        self.add_static_items([
            Row(
                Button(text="-", callback_data="menu.opts.machine.net.minus"),
                Button(text=f"{frequency}"),
                Button(text="+", callback_data="menu.opts.machine.net.plus"),
            )
        ])
  
  
class MenuOptsBotKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 3
        self.home_menu = "menu"
        self.current_menu = "menu.opts.bot"
        self.previous_menu = "menu.opts"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="🗃 Отправить логи", callback_data="menu.opts.bot.log")),
            Row(Button(text="❌ Выключить", callback_data="menu.opts.bot.poweroff"))
        ])
  
        
class MenuOptsAccessKeyboard(Keyboard):
    def __init__(self, generator, count: int) -> None:
        super().__init__()
        self.depth = 3
        self.home_menu = "menu"
        self.current_menu = "menu.opts.access"
        self.previous_menu = "menu.opts"
        self.rows_per_page = 5
        self.add_dynamic_items(
            generator,
            UserRow,
            count
        )
        

class MenuEtcKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 2
        self.home_menu = "menu"
        self.current_menu = "menu.etc"
        self.previous_menu = "menu"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="📸 Скриншот", callback_data="menu.etc.screen")),
            Row(Button(text="📝 Заметки", callback_data="menu.etc.note.pg_1")),
        ])
        

class MenuEtcNoteKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 3
        self.home_menu = "menu"
        self.current_menu = "menu.etc.note"
        self.previous_menu = "menu.etc"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="🆗 Продолжить", callback_data="menu.etc.note.name.pg_1"))
        ])
        

class MenuEtcNoteNameKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 4
        self.home_menu = "menu"
        self.current_menu = "menu.etc.note.name"
        self.previous_menu = "menu.etc"
        self.rows_per_page = 5
        

class MenuAboutKeyboard(Keyboard):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 2
        self.home_menu = "menu"
        self.current_menu = "menu.about"
        self.previous_menu = "menu"
        self.rows_per_page = 5
        self.add_static_items([
            Row(Button(text="📢 Telegram", url="https://t.me/sneppi_coding_channel")),
            Row(Button(text="💬 GitHub", url="https://github.com/Sn3ppi/remote-pc")) 
        ])
