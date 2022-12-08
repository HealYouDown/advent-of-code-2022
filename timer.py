from timeit import default_timer
from typing import Callable


def timer(func: Callable):
    def wrapper(*args, **kwargs):
        start = default_timer()
        res = func(*args, **kwargs)
        print((f"{func.__name__}: {round((default_timer() - start) * 1000, 4)}"))
        return res
    return wrapper
