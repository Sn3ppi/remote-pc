import time
from threading import Thread

from app.config.tmp import stop_sig
from models.tg.bot.basic import TGBotBasic

class TGBotLoop(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name = "TG Bot Loop"
        
    def run(self) -> None:
        bot = TGBotBasic()
        bot.start()
        while not stop_sig.is_set():
            time.sleep(0.1)
        bot.stop()