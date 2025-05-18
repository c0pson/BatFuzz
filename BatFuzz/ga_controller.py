from .genetic_algorithm import GeneticAlgorithm
from .type_defs import Fuzzable

from typing import Any, Callable, Type, Union

class GAController:
    def __init__(self, fuzz_target: Fuzzable) -> None:
        self.fuzz_target: Fuzzable = fuzz_target
        self.genetic_algorithms: list[GeneticAlgorithm[Any]] = []
        self._generation_cycle_time: int = 0
        self._generation: int = 0
        self._found_bugs: int = 0
        self._found_bugs_types: set[Exception] = set()

    def mutate_all(self) -> None:
        pass

    def crossover_all(self) -> None:
        pass

    def select_all(self) -> None:
        pass

    def handle_generation_errors(self) -> None:
        pass

    def run(self) -> None:
        pass

    @property
    def generation_cycle_time(self) -> int:
        return self._generation_cycle_time

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def found_bugs(self) -> int:
        return self._found_bugs

    @property
    def found_bugs_types(self) -> set[Exception]:
        return self._found_bugs_types
