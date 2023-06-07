import json

from database.common.connector import sql_request

def set_network(download: int, upload: int, last_update: float) -> None:
    '''Добавляет в БД данные об Интернет-соединении.'''
    sql_request('''UPDATE stats SET value=json_set(value, 
                    "$.network.download", ?,
                    "$.network.upload", ?, 
                    "$.network.last_update", ?) 
                WHERE name="stats"''', 
                (download, 
                 upload, 
                 last_update))
    

def get_network() -> list | None:
    '''Извлекает из БД данные об Интернет-соединении.'''
    return sql_request('''SELECT json_extract(value, 
                    "$.network.last_update",
                    "$.network.download",
                    "$.network.upload"       
                ) FROM stats WHERE name="stats"''',
                fetchall=True)[0][0]
    

def set_sensors(
    cpu_load: float,
    last_update: float,
    memory: dict,
    cpu_temperature: float,
    gpu_temperature: float,
    ram_free: int,
    ram_total: int,
    ram_percent: int,
    uptime: float
    ) -> None:
    '''Добавляет в БД данные о состоянии системы.'''
    sql_request('''UPDATE stats SET value=json_set(value, 
                    "$.sensors.cpu_load", ?,
                    "$.sensors.last_update", ?,
                    "$.sensors.memory", ?,
                    "$.sensors.temperatures.cpu", ?,
                    "$.sensors.temperatures.gpu", ?,
                    "$.sensors.ram.total", ?,
                    "$.sensors.ram.free", ?,
                    "$.sensors.ram.percent", ?,
                    "$.uptime", ?
                    ) WHERE name="stats"''', 
                (cpu_load,
                 last_update,
                 json.dumps(memory),
                 cpu_temperature,
                 gpu_temperature,
                 ram_free,
                 ram_total,
                 ram_percent,
                 uptime))


def get_sensors() -> list | None:
    '''Извлекает из БД данные о состоянии системы.'''
    return sql_request('''SELECT json_extract(value, 
                    "$.sensors.last_update",
                    "$.sensors.cpu_load",
                    "$.sensors.temperatures.cpu",
                    "$.sensors.temperatures.gpu",
                    "$.sensors.memory",
                    "$.sensors.ram.free",
                    "$.sensors.ram.total",
                    "$.sensors.ram.percent",
                    "$.uptime"
                ) FROM stats WHERE name="stats"''',
                fetchall=True)[0][0]