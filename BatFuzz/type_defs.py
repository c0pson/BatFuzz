from typing import TypeVar, Protocol, Any, Union, TypedDict
from enum import IntEnum

T = TypeVar('T')

class Fuzzable(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

Primitive = Union[str, int, float, bool, None]
FuzzableValue = Union[
    Primitive,
    list["FuzzableValue"],
    dict[str, "FuzzableValue"]
]

class FuzzableArguments(TypedDict, total=False):
    args: list[FuzzableValue]
    kwargs: dict[str, FuzzableValue]

class DEFAULT:
    GENERATIONS = 100
    POPULATION_SIZE = 50
    MUTATION_RATE = 0.01
    CROSSOVER_RATE = 0.7
