from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .tui import BatFuzz

class TUIObserver:
    def __init__(self, app: 'BatFuzz') -> None:
        self.app = app

    def update(self, event: str, data: dict) -> None:
        if event == "bug_found":
            bug_name = data["bug_name"]
            gen = data["generation"]
            self.app.notif.add(f"[{gen}] bug: {bug_name}")
            self.app.found_bugs.append(bug_name)
            self.app.unique_panel.bugs = list(set(self.app.found_bugs))
        elif event == "generation":
            self.app.gen_box.gen = data["generation"]
            self.app.gen_box.target_gen = data["target_generation"]
            self.app.gen_box.elapsed = data["elapsed"]
            self.app.loading_bar.progress = data["progress"]
            self.app.sys_stats.stats = data["system_stats"]
