from typing import Callable
from .type_defs import T

def fuzz(*types: type, **kwargs) -> Callable[[Callable[..., T]], Callable[..., T]]: ...
