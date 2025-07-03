import time
import inspect

def log(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()

        sig = inspect.signature(fn)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        arg_parts = []
        kwarg_parts = []

        for param in sig.parameters:
            if param in kwargs:
                kwarg_parts.append(f"{param}={bound.arguments[param]}")
            else:
                arg_parts.append(f"{param}={bound.arguments[param]}")

        with open('log.txt', 'a') as f:
            f.write(
                f"{fn.__name__}; args: {', '.join(arg_parts)}; "
                f"kwargs: {', '.join(kwarg_parts)}; "
                f"execution time: {end - start:.2f} sec.\n"
            )

        return result

    return wrapper