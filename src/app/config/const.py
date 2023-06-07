import os
import platform
import sys

SYSTEM_TYPE = platform.system()
if getattr(sys, 'frozen', False):
    MEIPASS = sys._MEIPASS
    ROOT_DIR = os.getcwd()
    CACHE_DIR = os.path.join(ROOT_DIR, 'cache')
    if SYSTEM_TYPE == 'Windows':
        OHW_DLL = os.path.join(MEIPASS, 'OpenHardwareMonitorLib.dll')
else:
    ROOT_DIR = os.path.dirname(__file__)
    CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ROOT_DIR))), 'cache')
    if SYSTEM_TYPE == 'Windows':
        OHW_DLL = os.path.join(os.path.dirname(os.path.dirname(ROOT_DIR)), 'machine', 'stats', 'OpenHardwareMonitorLib.dll')
BOT_DIR = os.path.join(CACHE_DIR, 'bot')
ENV_FILE = os.path.join(BOT_DIR, 'config.env')
LOG_FILE = os.path.join(BOT_DIR, 'log.txt')
DATABASE = os.path.join(BOT_DIR, 'pc.db')
FAVORITES_DIR = os.path.join(BOT_DIR, 'favorites')