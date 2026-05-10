'''Manages stdout output.'''

from typing import Any
from rich.console import Console, Group, RenderableType
from rich.text import TextType
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
    
    rich_print(table)

def display_pr_summary(data: Any):
    table = Table(title=f"PR Summary", border_style="green")
    table.add_column("Title", style="cyan", width=50)
    table.add_column("Files Changed", width=30)

    table.add_row(data["title"], str(len(data["files"])) + " files")

    rich_print(table)
    rich_print("\n[bold]Body:[/bold]\n" + (data["body"] or "—"))

    if data["files"]:
        rich_print("\n[bold]Changed Files:[/bold]")
        for f in data["files"]:
            rich_print(f"  - {f['path']}")

def display_run_status(data: Any):
    table = Table(title="CI Run Status", border_style="green")
    table.add_column("Branch", style="cyan")
    table.add_column("Status", width=12)
    table.add_column("Conclusion", width=12)

    for run in data:
        status = run["status"]
        conclusion = run["conclusion"]
        color = "yellow" if status == "queued" else "green" if conclusion == "success" else "red"
        table.add_row(
            run["headBranch"],
            f"[{color}]{status}[/{color}]",
            f"[{color}]{conclusion or '—'}[/{color}]",
        )

    rich_print(table)

def create_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
    )

def rich_print(text: RenderableType):
    console.print(text)

def rich_rule(title: TextType):
    console.rule(title)

def print_panel(
    title: str | None = None,
    *content: RenderableType,
    border_style: str = 'cyan'
):
    content_group = Group(*content)
    panel = Panel(content_group, title=title, border_style=border_style)
    rich_print(panel)
