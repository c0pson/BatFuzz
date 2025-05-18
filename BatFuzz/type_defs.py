from typing import TypeVar, Protocol, Any

T = TypeVar('T')

class Fuzzable(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
