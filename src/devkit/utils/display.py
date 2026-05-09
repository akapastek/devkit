'''Manages stdout output.'''

from typing import Any
from rich.console import Console, Group, RenderableType
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# ----- GLOBAL VARS -----

console = Console()

# ----- FUNCTIONS -----

def display_issues(data: Any):
    table = Table(title='Open Issues', border_style='green')
    table.add_column('#', style='cyan', width=6)
    table.add_column('Title', min_width=30)
    table.add_column('Labels', width=20)

    for issue in data:
        labels = ', '.join(l['name'] for l in issue.get('labels', []))
        table.add_row(str(issue['number']), issue['title'], labels or '—')
    
    console.print(table)

def create_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
    )

def rich_print(text: RenderableType):
    console.print(text)

def print_panel(
    title: str | None = None,
    *content: RenderableType,
    border_style: str = 'cyan'
):
    content_group = Group(*content)
    panel = Panel(content_group, title=title, border_style=border_style)
    rich_print(panel)
