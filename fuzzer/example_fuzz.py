from typing import Callable, Any
import random

from .values import SIZE

def generate_arg(type: type) -> Any:
    if type == int:
        return random.randrange(SIZE.MIN_INT, SIZE.MAX_INT)

def fuzz(*types: type, **kwargs) -> Callable:
    iterations: int = 100_000 if 'iterations' not in kwargs else (kwargs['iterations'] if isinstance(kwargs['iterations'], int) else 100_000)
    def decorator(f: Callable):
        def wrapper(*args, **kwargs):
            for _ in range(iterations):
                generated_args = [generate_arg(type) for type in types]
                try:
                    f(*generated_args)
                except OverflowError as e:
                    print(f'Failed with argument(s): ({', '.join(generated_args)}); which raised: {e}')
                finally:
                    # TODO: handle crashes not catch by the except block
                    pass
        return wrapper
    return decorator
