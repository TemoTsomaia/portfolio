from typing import Dict
import time

execution_time: Dict[str, float] = {}


def time_decorator(fn):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = fn(*args, **kwargs)
        end_time = time.time()
        execution_time[fn.__name__] = end_time - start_time
        return result
    return wrapper

