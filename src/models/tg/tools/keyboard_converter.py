from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
        
class KeyboardToTg(InlineKeyboardMarkup):
    def __init__(self, keyboard: list) -> None:
        super().__init__()
        self.row_width = 5
        for row in keyboard:
            self.add(*[InlineKeyboardButton(**button) for button in row])