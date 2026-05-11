'''Contains all the devkit commands.'''

import typer

from devkit.commands import github, ai, workflow
from devkit.utils.display import rich_print, print_panel
from devkit.utils.validation import check_tools

# ----- GLOBAL VARS -----

app = typer.Typer(
    name='devkit',
    help='AI-powered developer toolkit',
    rich_markup_mode='rich',
)

# Register sub-apps
app.add_typer(github.app, name='gh', help='GitHub operations')
app.add_typer(ai.app, name='ai', help='AI tools (Copilot, Gemini, Mistral)')
app.add_typer(workflow.app, name='workflow', help='End-to-end dev workflows')

# ----- FUNCTIONS -----

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    '''AI-powered developer toolkit'''
    check_tools()
    if ctx.invoked_subcommand is None:
        print_panel(None, 'Welcome to [bold cyan]devkit[/bold cyan]')
        rich_print(ctx.get_help())

# ----- MAIN -----

# not executed if installed via 'pip install -e .', sinces the latter uses 'app' directly as the entry point
if __name__ == '__main__':
    print('inside __main__')
    app()
