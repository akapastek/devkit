'''Contains all the devkit commands.'''

import typer
import subprocess
from typing import Annotated

from devkit.utils.gh import gh_json, gh
from devkit.commands.ai import Copilot, Gemini, Mistral
from devkit.utils.display import rich_print, print_panel, create_progress, display_issues
from devkit.utils.validation import confirm

# ----- GLOBAL VARS -----

app = typer.Typer()

# ----- FUNCTIONS -----

@app.command()
def issues(
    repo: Annotated[str | None, typer.Option(help='Targeted repository.')] = None,
    limit: Annotated[int, typer.Option(help='Number of issues displayed.')] = 10,
):
    '''gh issue list as a rich table, colored by state.'''
    # data = gh_json('issue', 'list', '--json', 'title,author,createdAt,state', pretty=True)
    # print(data)
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    if repo is not None:
        args += ['--repo', repo]
    
    data = gh_json(*args)
    display_issues(data)

@app.command()
def explain(command: Annotated[str, typer.Argument(..., help='Shell command to explain')]):
    '''Ask Copilot CLI to explain a shell command.'''
    result_text = Copilot.explain(command)
    print_panel('[purple]Copilot Explaination[/purple]', result_text)

@app.command()
def suggest(command: Annotated[str, typer.Argument(..., help='Task to accomplish')]):
    '''Ask Copilot CLI to suggest a command.'''
    result_text = Copilot.suggest(command)
    print_panel('[purple]Copilot Suggestion[/purple]', result_text)

@app.command()
def review(
    pr_number: Annotated[int, typer.Argument(..., help='PR number to review')],
):
    '''AI-powered code review of a pull request.'''
    with create_progress() as progress:
        prog_task = progress.add_task('Fetching PR diff...')
        diff = gh('pr', 'diff', str(pr_number))
        pr_info = gh_json('pr', 'view', str(pr_number), '--json', 'title,body')

        progress.update(prog_task, description='Running AI review...')
        result = Gemini.review(pr_info["title"], diff)

    print_panel(f'[cyan]AI Review — PR #{pr_number}[/cyan]', result)

@app.command()
def commit():
    '''Generate a commit message from staged changes using AI.'''
    diff = subprocess.check_output(['git', 'diff', '--cached'], text=True)
    if not diff.strip():
        rich_print('[yellow]No staged changes.[/yellow]')
        raise typer.Exit()
    
    suggested = Mistral.commit(diff)
    print_panel('[green]Suggested Commit Message[/green]', suggested)

    confirm('Use this message?')
    subprocess.run(['git', 'commit', '-m', suggested])

# ----- MAIN -----

# not executed if installed via 'pip install -e .', sinces the latter uses 'app' directly as the entry point
if __name__ == '__main__':
    print('inside __main__')
    app()
