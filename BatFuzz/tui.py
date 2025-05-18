from __future__ import annotations
from datetime import datetime
import itertools

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer

from .widgets import (
    Banner, LoadingBar, GenTimeBox,
    NotificationPanel, SysStatsPanel, UniqueBugsPanel
)

class BatFuzz(App):
    CSS = """
        Screen { background: #1b1b1b; color: white; }

        #banner { height: 8; }

        #top-bar     { layout: horizontal; height: 3; }
        #loading_bar { width: 70%; }
        #gen_box     { width: 30%; }

        #main-grid { layout: horizontal; height: 1fr; }
        #notif     { width: 50%; overflow-y: scroll; }
        #sys       { width: 15%; }
        #unique    { width: 35%; }

        Footer { dock: bottom; }
    """
    BINDINGS = [("q", "quit", "Quit"), ("r", "reset", "Reset")]

    FAKE_BUG_TYPES = [
        "NullPointer", "BufferOverflow", "RaceCondition", "UseAfterFree",
        "IntegerOverflow", "OffByOne", "MemoryLeak", "StackSmash",
        "UncaughtException", "Segfault"
    ]

    def compose(self) -> ComposeResult:
        yield Banner(id="banner")
        with Horizontal(id="top-bar"):
            self.loading_bar = LoadingBar(id="loading_bar")
            yield self.loading_bar
            self.gen_box = GenTimeBox(id="gen_box")
            yield self.gen_box
        with Horizontal(id="main-grid"):
            self.notif = NotificationPanel(id="notif")
            yield self.notif
            self.sys_stats = SysStatsPanel(id="sys")
            yield self.sys_stats
            self.unique_panel = UniqueBugsPanel(id="unique")
            yield self.unique_panel
        yield Footer()

    def fake_stats(self):
        while True:
            for gen in itertools.count(1):
                yield gen

    def on_mount(self) -> None:
        self.start_time = datetime.now()
        self._fake_iter = self.fake_stats()
        self.found_bugs: list = []
        self.refresh_count = 0
        self.set_interval(0.2, self.refresh_stats)

    def refresh_stats(self) -> None:
        now = datetime.now()
        pct = ((now - self.start_time).total_seconds() % 10) / 10
        self.loading_bar.progress = pct

        self.gen_box.gen = int(pct * 100)
        self.gen_box.elapsed = now - self.start_time

        self.sys_stats.stats = {
            "RAM": "3.1 GB / 8 GB",
            "CPU": "42 %",
            "GPU": "N/A",
        }
        self.refresh_count += 1
        if self.refresh_count % 10 == 0:
            if len(self.found_bugs) < len(self.FAKE_BUG_TYPES):
                next_bug = self.FAKE_BUG_TYPES[len(self.found_bugs)]
                self.found_bugs.append(next_bug)
                self.notif.add(f"[{self.gen_box.gen}] new bug found: {next_bug}")
                self.unique_panel.bugs = list(self.found_bugs)  # Force reactivity

    def action_reset(self) -> None:
        self.start_time = datetime.now()
        self._fake_iter = self.fake_stats()
        self.notif.update("")
        self.found_bugs = []
        self.unique_panel.bugs = []

def run() -> None:
    BatFuzz().run()
