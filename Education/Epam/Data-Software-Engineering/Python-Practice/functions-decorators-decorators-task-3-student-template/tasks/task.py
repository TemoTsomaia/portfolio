from functools import wraps

def validate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if any(i < 0 or i > 256 for i in list(args) + list(kwargs.values())):
            return "Function call is not valid!"
        return func(*args, **kwargs)
    return wrapper

@validate
def set_pixel(x: int, y: int, z: int) -> str:
  return "Pixel created!"
