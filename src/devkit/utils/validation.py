'''Manages data validation, user validation and stderr output.'''

import typer
from rich.console import Console, RenderableType
from rich.text import TextType
from rich.prompt import Confirm
from datetime import date

# ----- GLOBAL VARS -----

err_console = Console(stderr=True) # Write errors to stderr

# ----- FUNCTIONS -----

def rich_error(text: RenderableType):
    err_console.print(text)

def confirm(text: TextType):
    confirmed = Confirm.ask(text, default=False)
    if not confirmed:
        err_console.print('[yellow]Cancelled.[/yellow]')
        raise typer.Exit()
