from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic

from .chromosome import Chromosome
from .type_defs import T

class GeneticAlgorithm(ABC, Generic[T]):
    _chromosomes: list[Chromosome[T]]
    _magic_values: list[T]
    _mutation_tokens: dict[str, T]

    def __init__(self) -> None:
        self._chromosomes = []
        self._magic_values = []
        self._mutation_tokens = {}
        self._score = 0.0
        self._time = 0.0
        self._generation_iteration = 0
        self._population_size = 0

    @abstractmethod
    def generate_initial_population(self) -> None:
        pass

    @abstractmethod
    def mutate_chromosomes(self) -> None:
        pass

    @abstractmethod
    def populations_crossover(self) -> None:
        pass

    @abstractmethod
    def populations_selection(self) -> None:
        pass

    @abstractmethod
    def preserve_population_diversity(self) -> None:
        pass

    @abstractmethod
    def co_evolute_population(self, other: GeneticAlgorithm[T]) -> None:
        pass

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, value: float) -> None:
        self._score = value

    @property
    def time(self) -> float:
        return self._time

    @property
    def generation(self) -> int:
        return self._generation_iteration

    @property
    def population_size(self) -> int:
        return self._population_size
