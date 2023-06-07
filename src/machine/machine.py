from machine.stats_updater import *

def machine_start() -> None:
    '''Запускает потоки обновления данных.'''
    AutoUpdateNetwork().start()
    AutoUpdateSensors().start()