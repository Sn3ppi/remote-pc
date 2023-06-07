import random
import os

__all__ = [
    'set_seed',
    'random_number'
]

def set_seed() -> None:
    random.seed(os.urandom(8).hex())
    

def random_number(start: int, end: int) -> int:
    return random.randrange(start, end)