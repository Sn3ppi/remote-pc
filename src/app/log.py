import logging

from app.folders import log_file

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console = logging.StreamHandler()
console.setFormatter(formatter)

file = logging.FileHandler(filename=log_file(), encoding='utf-8')    
file.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file)