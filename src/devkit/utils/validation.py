'''Manages data validation, user validation and stderr output.'''

import typer
import shutil
from rich.console import Console, RenderableType
from rich.text import TextType
from rich.prompt import Confirm
from datetime import date

# ----- GLOBAL VARS -----

err_console = Console(stderr=True) # Write errors to stderr

REQUIRED_TOOLS = {
 'gh': 'Install from https://cli.github.com',
 'fzf': 'brew install fzf or apt install fzf',
 'bat': 'brew install bat or apt install bat',
 'delta': 'brew install git-delta',
}

# ----- FUNCTIONS -----

def check_tools():
    missing = {t: hint for t, hint in REQUIRED_TOOLS.items() if not shutil.which(t)}
    if missing:
        err_console.print('[red]Missing required tools:[/red]')
        for tool, hint in missing.items():
            err_console.print(f' [cyan]{tool}[/cyan] — {hint}')
        raise SystemExit(1)

def validate_config(cfg: dict):
    '''Verifies configuration has correct format and values.'''
    def aux(key: str, is_in: list[str]):
        val = str(cfg.get(key, None))
        if not val in is_in:
            rich_error(f"[red]Error :[/red] '{val}' is not a valid value for key config '{key}'.\nValid values: {is_in}.")
            exit(1)
    
    to_verify: list[tuple[str, list[str]]] = [
        ("ai_tool", ["mistral", "copilot", "gemini"]),
        ("theme", ["light", "dark", "None"]),
        ("show_spinner", ["False", "True", "None"]),
    ]
    for key, is_in in to_verify:
        aux(key, is_in)

def rich_error(text: RenderableType):
    err_console.print(text)

def confirm(text: TextType):
    confirmed = Confirm.ask(text, default=False)
    if not confirmed:
        err_console.print('[yellow]Cancelled.[/yellow]')
        raise typer.Exit()
