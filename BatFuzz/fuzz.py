from typing import Callable, TypeVar, Any
from .type_defs import DEFAULT, Fuzzable, FuzzableArguments
from .ga_controller import GAController
from .observer import TUIObserver
from .tui import BatFuzz

T = TypeVar('T')

def fuzz(*types: type, **kwargs) -> Callable[[Callable[..., T]], Callable[..., T]]:
    generations: int = kwargs.get("generations", DEFAULT.GENERATIONS)
    
    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs):
            app = BatFuzz()
            controller = GAController(f, [types, kwargs], generations)
            observer = TUIObserver(app)
            controller.add_observer(observer)
            app.ga_controller = controller
            app.ga_observer = observer
            app.run()
            return
        return wrapper
    return decorator
