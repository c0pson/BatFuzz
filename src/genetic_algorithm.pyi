from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, List, Dict
from .chromosome import Chromosome
from .type_defs import T

class GeneticAlgorithm(ABC, Generic[T]):
    _chromosomes: List[Chromosome]
    _magic_values: List[T]
    _mutation_tokens: Dict[str, T]

    @abstractmethod
    def generate_initial_population(self) -> None: ...

    @abstractmethod
    def mutate_chromosomes(self) -> None: ...

    @abstractmethod
    def populations_crossover(self) -> None: ...

    @abstractmethod
    def populations_selection(self) -> None: ...

    @abstractmethod
    def preserve_population_diversity(self) -> None: ...

    @abstractmethod
    def co_evolute_population(self, other: GeneticAlgorithm[T]) -> None: ...

    @property
    def score(self) -> float: ...

    @score.setter
    def score(self, value: float) -> None: ...

    @property
    def time(self) -> float: ...

    @property
    def generation(self) -> int: ...

    @property
    def population_size(self) -> int: ...
