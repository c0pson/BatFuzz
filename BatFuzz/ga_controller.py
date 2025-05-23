from datetime import datetime, timedelta
from time import sleep

from .genetic_algorithm import GeneticAlgorithm
from .type_defs import Fuzzable, FuzzableArguments
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .observer import Observer

class GAController:
    def __init__(self, fuzz_target: Fuzzable, arguments: FuzzableArguments, target_generation: int) -> None:
        self.fuzz_target: Fuzzable = fuzz_target
        self.genetic_algorithms: list[GeneticAlgorithm[Any]] = []
        self._arguments: FuzzableArguments = arguments
        self._generation_cycle_time: int = 0
        self._generation: int = 0
        self._found_bugs: int = 0
        self._found_bugs_types: set[Exception] = set()
        self._target_generation: int = target_generation
        self._observers: list['Observer'] = []
        self._start_time = datetime.now()
        self._current_progress: float = 0.0
        self._system_stats: dict[str, str] = {
            'RAM': '0.0 GB / 0.0 GB',
            'CPU': '0 %',
        }

    def notify(self, event: str, data: dict) -> None:
        for observer in self._observers:
            observer.update(event, data)

    def add_observer(self, observer: 'Observer') -> None:
        self._observers.append(observer)

    def mutate_all(self) -> None:
        pass

    def crossover_all(self) -> None:
        pass

    def select_all(self) -> None:
        pass

    def handle_generation_errors(self) -> None:
        pass

    def run(self) -> None:
        self._start_time = datetime.now()
        for gen in range(self._target_generation):
            self._generation = gen
            self._current_progress = (gen+1) / self._target_generation if self._target_generation > 0 else 0
            self._update_system_stats()
            self.notify('generation', {
                'generation': gen+1,
                'target_generation': self._target_generation,
                'progress': self._current_progress,
                'elapsed': datetime.now() - self._start_time,
                'system_stats': self._system_stats
            })
            try:
                self.fuzz_target()
            except Exception as bug:
                self._found_bugs += 1
                self._found_bugs_types.add(bug)
                self.notify('bug_found', {
                    'bug': bug,
                    'bug_name': type(bug).__name__,
                    'generation': gen,
                    'total_bugs': self._found_bugs,
                    'arguments': None
                })

    def _update_system_stats(self) -> None:
        import random
        ram_usage = 2.0 + (self._generation % 10) / 10
        ram_total = 8.0
        cpu_usage = 30 + (self._generation % 40)
        
        self._system_stats = {
            'RAM': f'{ram_usage:.1f} GB / {ram_total:.1f} GB',
            'CPU': f'{cpu_usage} %',
        }

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
        
    @property
    def progress(self) -> float:
        return self._current_progress
        
    @property
    def elapsed_time(self) -> timedelta:
        return datetime.now() - self._start_time
        
    @property
    def system_stats(self) -> dict[str, str]:
        return self._system_stats
