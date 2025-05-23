from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import sys
import os

if TYPE_CHECKING:
    from .tui import BatFuzz

class Observer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def update(self, event: str, data: dict) -> None:
        pass

class TUIObserver(Observer):
    def __init__(self, app: 'BatFuzz') -> None:
        self.app = app

    def update(self, event: str, data: dict) -> None:
        if event == 'bug_found':
            bug_name = data['bug_name']
            gen = data['generation']
            self.app.notif.add(f'[{gen}] bug: {bug_name}')
            self.app.found_bugs.append(bug_name)
            self.app.unique_panel.bugs = list(set(self.app.found_bugs))
        elif event == 'generation':
            self.app.gen_box.gen = data['generation']
            self.app.gen_box.target_gen = data['target_generation']
            self.app.gen_box.elapsed = data['elapsed']
            self.app.loading_bar.progress = data['progress']
            self.app.sys_stats.stats = data['system_stats']

class LoggingObserver(Observer):
    def __init__(self, func_name: str, log_path: Optional[str] = None):
        if log_path:
            self.log_path: str = log_path
        else:
            self.log_path = self.create_log_file(func_name)

    def create_log_file(self, func_name: str) -> str:
        user_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        log_dir = os.path.join(user_dir, 'batfuzz_logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file_name = f'{datetime.now().strftime(f'{func_name}_%Y-%m-%d_%H-%M-%S')}.batlog'
        return os.path.join(log_dir, log_file_name)

    def prepare_log_file(self, file_name: str, func_name: str) -> None:
        with open(self.log_path, 'a') as f:
            f.write(f'{'-'*30}\nPath: {file_name}\nFunction: {func_name}\n{'-'*30}')

    def update(self, event: str, data: dict) -> None:
        with open(self.log_path, 'a') as f:
            if event == 'bug_found':
                f.write(f'[{data['generation']}] Bug found: {type(data['bug']).__name__} with arguments ({data['arguments']})\n')
