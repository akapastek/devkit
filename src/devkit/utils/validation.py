'''Manages data validation, user validation and stderr output.'''

import typer
from rich.console import Console
from rich.prompt import Confirm
from datetime import date

# ----- GLOBAL VARS -----

err_console = Console(stderr=True) # Write errors to stderr

# ----- FUNCTIONS -----

def confirm(text: str):
    confirmed = Confirm.ask(text, default=False)
    if not confirmed:
        err_console.print('[yellow]Cancelled.[/yellow]')
        raise typer.Exit()
