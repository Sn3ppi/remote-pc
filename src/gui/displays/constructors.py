from utils.manystring import ManyString

'''Названия отдельных пунктов меню. Может быть использовано в качестве заголовков для окон меню и кнопок.'''

headlines = {
    "menu": "🏠 Меню",
    "sys": "🖥 Система",
    "net": "🌐 Интернет",
    "progs": "🕹 Быстрый запуск",
    "opts": "⚙️ Настройки",
    "machine": "🖥 Компьютер",
    "bot": "🤖 Бот",
    "reset": "❌ Сброс",
    "access": "👤 Пользователи",
    "etc": "➡️ Ещё",
    "screen": "📸 Скриншоты",
    "note": "📝 Заметки",
    "name": "📝 Название",
    "about": "ℹ️ О нас"
}


class Display:
    '''Конструктор сообщений.'''
    def __init__(self) -> None:
        super().__init__()
        self._header = None
        self._description = None
        
    def __repr__(self) -> str:
        text = ManyString()
        text.enter(self._header)
        text.enter(self._description, space=2)
        return str(text)
 
    def set_header(self, inner_name: str, separator: str=".", translator: str=headlines) -> None:
        self._header = " > ".join([translator[key] for key in inner_name.split(sep=separator)])
        
    def set_description(self, text: str) -> None:
        self._description = text