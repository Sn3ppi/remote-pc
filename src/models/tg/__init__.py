from models.tg.bot import TGBotLoop

def tg_start() -> None:
    bot = TGBotLoop()
    bot.start()