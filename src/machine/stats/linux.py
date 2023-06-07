import time
import psutil

from speedtest import Speedtest

__all__ = [
    'get_memory', 
    'get_network_speed', 
    'get_ram', 
    'get_uptime', 
    'get_timestamp', 
    'get_cpu_load',
    'get_temperatures' 
]

def get_temperatures() -> list:
    '''Получает температуру видеокарты и процессора соответственно.'''
    results = [None, None]
    data = psutil.sensors_temperatures()
    for i, device in enumerate(data):
        results[i] = data[device][0].current
    return results


def get_memory() -> dict:
    '''Получает общий объём, оставшийся объём и занятый в процентном отношении объём памяти на смонтированных разделах подключенных дисков.'''
    disks = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        partition_name = partition.device.replace('\\', '')
        disks[partition_name] = {}
        disks[partition_name]["total"] = disk_usage[0]
        disks[partition_name]["free"] = disk_usage[0]-disk_usage[1]
        disks[partition_name]["percent"] = 100-disk_usage[3]
    return disks
            

def get_network_speed() -> list:
    '''Получает данные об Интернет-соединении.'''
    data = [None, None, None]
    try:
        net = Speedtest()
        data = [net.download(), net.upload(), time.time()]
    except Exception as e:
        print(e)
    return data


def get_ram() -> list:
    '''Получает данные об общем, свободном объёме и объёме в процентном отношении памяти в ОЗУ.'''
    ram = psutil.virtual_memory()
    return [ram[0], ram[1], 100-ram[2]]
    

def get_uptime() -> float:
    '''Возвращает кол-во секунд, прошедших с момента запуска машины.'''
    return time.time() - psutil.boot_time()


def get_timestamp() -> str:
    '''Возвращает timestamp в секундах.'''
    return time.time()


def get_cpu_load() -> float:
    '''Возвращает общий % нагрузки на процессор.'''
    return psutil.cpu_percent()