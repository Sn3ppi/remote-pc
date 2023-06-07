'''Инструмент для удобного создания многострочной строки.'''
class ManyString:
    def __init__(self, text='') -> None:
        self.text = text
        
    def enter(self, text, space: int=1) -> None:
        if isinstance(text, str):
            if self.text:
                spaces = "".join(["\n" for _ in range(space)])
                self.text = spaces.join([self.text, text])
            else:
                self.text = text
            
    def __repr__(self) -> str:
        return self.text