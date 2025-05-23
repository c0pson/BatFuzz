from typing import Callable
from .type_defs import DEFAULT, T
from .ga_controller import GAController
from .observer import TUIObserver, LoggingObserver
from .tui import BatFuzz

def fuzz(*types: type, **kwargs) -> Callable[[Callable[..., T]], Callable[..., T]]:
    generations: int = kwargs.get('generations', DEFAULT.GENERATIONS)
    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs):
            app = BatFuzz()
            controller = GAController(f, [types, kwargs], generations)
            tui_observer = TUIObserver(app)
            log_observer = LoggingObserver(f.__name__)
            controller.add_observer(tui_observer)
            controller.add_observer(log_observer)
            app.ga_controller = controller
            app.ga_observer = tui_observer
            app.log_observer = log_observer
            app.run()
            return
        return wrapper
    return decorator
