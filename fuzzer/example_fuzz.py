from typing import Callable, Any
import random

from .enums import SIZE
from .generator import GeneticGenerator

def generate_arg(type: type) -> Any:
    """Function creating random argument based on the type.
    Supported types:
    - int

    Args:
        type (type): type of the argument to generate.

    Returns:
        Any: Returns the generated argument with the same type as provided if supported.
    """
    if type == int:
        return random.randrange(SIZE.MIN_INT, SIZE.MAX_INT)
    raise ValueError(f'No implementation for type: {type}')

def fuzz(*types: type, **kwargs) -> Callable:
    """Decorator for fuzz testing a function by repeatedly calling it with randomly 
    generated arguments of the specified types.

    Args:
        *types (type): Types of arguments to generate for the decorated function.
        **kwargs: Optional keyword arguments:
            - iterations (int): Number of times to call the function. Defaults to 100_000_000.

    Returns:
        Callable: A wrapped function that runs fuzz testing.
    """
    iterations: int = 100_000_000 if 'iterations' not in kwargs else (kwargs['iterations'] if isinstance(kwargs['iterations'], int) else 100_000_000)
    def decorator(f: Callable):
        def wrapper(*args, **kwargs):
            generation = GeneticGenerator() # here the GeneticGenerator will be used
            for _ in range(iterations):
                generated_args = [generate_arg(type) for type in types]
                try:
                    f(*generated_args)
                except Exception as e:
                    # in general don't use general Exception as its bad practice
                    # but in this case its unavoidable as we dont know how the passed function might misbehave
                    args_as_str = ', '.join(str(arg) for arg in generated_args)
                    print(f'Failed with argument(s): ({args_as_str}); which raised: {e}')
                # generation.next_gen() # will be used after implementation
            print(f'Fuzzing of function "{f.__name__}" completed.')
        print(f'Fuzzing of function "{f.__name__}" started.')
        return wrapper
    return decorator
