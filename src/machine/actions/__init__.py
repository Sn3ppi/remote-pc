from app.config.const import SYSTEM_TYPE

if SYSTEM_TYPE == "Windows":
    from machine.actions.windows import *
elif SYSTEM_TYPE == "Linux":
    from machine.actions.linux import *