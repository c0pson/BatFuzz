from __future__ import annotations
from datetime import timedelta
from typing import Dict, List

from rich.console import RenderableType
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.align import Align
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

class Banner(Widget):
    def render(self) -> RenderableType:
        ascii_logo = r"""
  /\     ______       _  ______             
 / \'._  | ___ \     | | |  ___|            
/_.''._'-' |_/ / __ _| |_| |_ _   _ ________
| \_ / `;  ___ \/ _` | __|  _| | | |_  /_  /
 \/ `\___  |_/ / (_| | |_| | | |_| |/ / / / 
         \____/ \__,_|\__\_|  \__,_/___/___|
"""
        return Align.center(Text(ascii_logo, style="bold cyan"))

class LoadingBar(Widget):
    progress = reactive(0.0)
    PROG = Progress(
        TextColumn("[bold]Generation Progress:"),
        BarColumn(bar_width=None, style="cyan"),
        TextColumn("{task.percentage:>3.0f}%"),
        expand=True,
    )
    _tid = PROG.add_task("fuzzing", total=100)

    def render(self) -> RenderableType:
        self.PROG.update(self._tid, completed=self.progress * 100)
        return Panel(
            self.PROG,
            title="Fuzzing Progress",
            border_style="cyan",
            padding=(0, 1),
            height=3,
        )

class GenTimeBox(Static):
    gen = reactive(0)
    target_gen = reactive(0)
    elapsed = reactive(timedelta())

    def render(self) -> RenderableType:
        progress_percentage = (self.gen / self.target_gen * 100) if self.target_gen > 0 else 0
        txt = Text(f"GEN {self.gen}/{self.target_gen} ({progress_percentage:.1f}%)\nTIME {self.elapsed}", justify="center")
        return Panel(txt, border_style="cyan", height=3)

class NotificationPanel(Static):
    def add(self, msg: str) -> None:
        lines = (self.renderable.plain.splitlines() if self.renderable else [])[-200:]  # type: ignore
        lines.append(msg)
        self.update(Text("\n".join(lines), style="white"))

class SysStatsPanel(Widget):
    stats: reactive[Dict[str, str]] = reactive({})

    def render(self) -> RenderableType:
        table = Table.grid(padding=(0, 1))
        for k, v in self.stats.items():
            table.add_row(Text(k, style="bold"), Text(v))
        return Panel(table, title="SYSTEM RESOURCES", border_style="cyan")

class UniqueBugsPanel(Widget):
    bugs: reactive[List[str]] = reactive([])

    def render(self) -> RenderableType:
        if not self.bugs:
            txt = Text("No bugs found yet.", style="dim", justify="center")
        else:
            txt = Text("\n".join(self.bugs), style="bold red", justify="left")
        return Panel(txt, title="UNIQUE bugs", border_style="cyan")
