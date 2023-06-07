from app.config.const import SYSTEM_TYPE

if SYSTEM_TYPE == "Windows":
    from machine.stats.windows import *
elif SYSTEM_TYPE == "Linux":
    from machine.stats.linux import *