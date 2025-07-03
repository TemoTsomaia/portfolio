from functools import wraps


def decorator_apply(lambda_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return lambda_func(result)
        return wrapper
    return decorator
    pass


@decorator_apply(lambda user_id: user_id + 1)
def return_user_id(num: int) ->int:
    return num
