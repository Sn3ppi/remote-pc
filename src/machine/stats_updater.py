import time
from threading import Thread

from app.config.tmp import stop_sig
from database.tables.machine import get_net_autoupdate_frequency, get_sys_autoupdate_frequency
from database.tables.stats import set_network, set_sensors
from machine.stats import *

__all__ = ['AutoUpdateSensors', 'AutoUpdateNetwork']

class UpdateSensors(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name="Sensors Data Updating"
        self.daemon = True
        
    def run(self) -> None:
        set_sensors(
            get_cpu_load(),
            get_timestamp(),
            get_memory(),
            *get_temperatures(),
            *get_ram(),
            get_uptime(), 
        )


class UpdateNetwork(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name="Network Data Updating"
        self.daemon = True
        
    def run(self) -> None:
        set_network(*get_network_speed())


class AutoUpdateSensors(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name="Autoupdating Sensors Data"
        self.daemon = True
        
    def run(self) -> None:
        while not stop_sig.is_set():
            frequency = get_sys_autoupdate_frequency()
            if frequency:
                UpdateSensors().run()
                time.sleep(frequency)
            else:
                time.sleep(1)
            
            
class AutoUpdateNetwork(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.name="Autoupdating Network Data"
        self.daemon = True
        
    def run(self) -> None:
        while not stop_sig.is_set():
            frequency = get_net_autoupdate_frequency()
            if frequency:
                UpdateNetwork().run()
                time.sleep(frequency)
            else:
                time.sleep(1)