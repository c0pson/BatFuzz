from typing import Generic
from sys import getsizeof

from .type_defs import T

class Chromosome(Generic[T]):
    def __init__(self, genes: T) -> None:
        self.genes: T = genes
        self.size: int = getsizeof(genes)
        self.fitness: float = 0.0
        self.age: int = 0
