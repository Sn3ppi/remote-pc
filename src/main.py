import signal
import time
from threading import enumerate as get_threads, current_thread

from app.config.const import SYSTEM_TYPE
from app.config.tmp import stop_sig
from app.register import validate_keys
from database.common.table import create_table
from machine.machine import machine_start
from models.tg import tg_start

def stop_handler(*args, **kwargs) -> None:
    stop_sig.set()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_handler)
    if SYSTEM_TYPE == 'Linux':
        signal.signal(signal.SIGTERM, stop_handler)
    validate_keys()
    create_table()
    tg_start()
    machine_start()
    while not stop_sig.is_set():
        time.sleep(0.1)
    for thr in get_threads():
        if not thr.daemon and thr != current_thread():
            thr.join()