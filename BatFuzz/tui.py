from __future__ import annotations
from datetime import datetime
from typing import Any, List, Optional

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
        #sys       { width: 20%; }
        #unique    { width: 30%; }

        Footer { dock: bottom; }
    """
    BINDINGS = [("q", "quit", "Quit")]

    loading_bar: LoadingBar
    gen_box: GenTimeBox
    notif: NotificationPanel
    sys_stats: SysStatsPanel
    unique_panel: UniqueBugsPanel
    found_bugs: List[str]
    ga_controller: Optional[Any] = None
    ga_observer: Optional[Any] = None

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

    def on_mount(self) -> None:
        self.start_time = datetime.now()
        self.found_bugs = []
        if self.ga_controller:
            self.gen_box.target_gen = self.ga_controller._target_generation
            self.run_controller()

    def setup_ga(self, fuzzable: Any, arguments: Any, generations: int) -> None:
        """Setup the GA controller and observer manually (if not using decorator)"""
        from .ga_controller import GAController
        from .observer import TUIObserver
        
        self.ga_controller = GAController(fuzzable, arguments, generations)
        self.ga_observer = TUIObserver(self)
        self.ga_controller.add_observer(self.ga_observer)

    def run_controller(self) -> None:
        """Run the GA controller in a separate thread"""
        import threading
        
        if self.ga_controller:
            thread = threading.Thread(target=self.ga_controller.run)
            thread.daemon = True
            thread.start()
