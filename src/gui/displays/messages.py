'''Прочие уведомления и предупреждения, предназначенные для отправки ботом в чаты.'''

from gui.displays.constructors import Display
from utils.manystring import ManyString

__all__ = [
    'UserProfile'
]

class UserProfile(Display):
    def __init__(self, data: list, outer_id: int, account_type: str) -> None:
        super().__init__()
        d = ManyString()
        
        registration_date = None if not data else str(data[0][0])
        inner_id = None if not data else data[0][1]
        level = None if not data else data[0][2]
        
        d.enter(f"🕒 Дата регистрации: {registration_date}")
        d.enter(f"👤 Внутренний ID: {inner_id}")
        d.enter(f"👤 Внешний ID: {outer_id}")
        d.enter(f"🌐 Тип аккаунта: {account_type}")
        d.enter(f"🔓 Уровень: {level}")
        self.set_description(str(d))