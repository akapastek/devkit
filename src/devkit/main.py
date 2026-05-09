'''Contains all the devkit commands.'''

import typer
import subprocess
from typing import Annotated

from devkit.utils.gh import gh_json, gh
from devkit.commands.ai import Copilot, Gemini, Mistral
from devkit.utils.display import (
    rich_print, print_panel, create_progress,
    display_issues, display_pr_summary, display_run_status
)
from devkit.utils.validation import confirm

# ----- GLOBAL VARS -----

app = typer.Typer()

# ----- NON-AI FEATURES -----

@app.command()
def issues(
    limit: Annotated[int, typer.Option(help='Max number of issues displayed.')] = 10,
    repo: Annotated[str | None, typer.Option(help='Targeted repository.')] = None
):
    '''List issues as a rich table, colored by state.'''
    # data = gh_json('issue', 'list', '--json', 'title,author,createdAt,state', pretty=True)
    # print(data)
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    if repo is not None:
        args += ['--repo', repo]
    
    data = gh_json(*args)
    display_issues(data)

@app.command()
def pr_summary(
    pr_number: Annotated[int, typer.Argument(..., help='Pull request #.')],
    repo: Annotated[str | None, typer.Option(help='Targeted repository.')] = None
):
    """Display title, body and modified files of a PR."""
    args = ["pr", "view", str(pr_number), "--json", "title,body,files"]
    if repo is not None:
        args += ["--repo", repo]
    
    data = gh_json(*args)
    display_pr_summary(data)

@app.command()
def start_feature(
    branch_name: Annotated[str, typer.Argument(..., help='New feature\'s branch name.')],
    repo: Annotated[str, typer.Argument(..., help='Targeted repository.')]
):
    """Fork repo and create a branch for the new feature."""
    gh("repo", "fork", repo, "--clone")

    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    rich_print(f"✅ Branch '{branch_name}' created and ready for the feature !")

@app.command()
def open_pr(
    title: Annotated[str, typer.Argument(..., help="PR title.")],
    base: Annotated[str, typer.Argument("main", help="Base branch (ex: tests).")],
    head: Annotated[str, typer.Argument(..., help="Source branch (ex: my-branch).")],
    body: Annotated[str, typer.Option(help="PR body.")] = "",
    repo: Annotated[str | None, typer.Option(help="Targeted repository.")] = None
):
    """Creates a PR."""
    args = ["pr", "create", "--title", title, "--body", body, "--fill", "--base", base, "--head", head]
    if repo is not None:
        args += ["--repo", repo]
    
    try:
        result = gh(*args)
        rich_print(f"✅ PR created : {result}")
    except subprocess.CalledProcessError as e:
        rich_print(f"❌ Error : {e.stderr.decode().strip()}", err=True)
        raise typer.Exit(1)

@app.command()
def run_status(
    limit: Annotated[int, typer.Option(help='Max number of issues displayed.')] = 10,
    repo: Annotated[str | None, typer.Option(help="Targeted repository.")] = None
):
    """Displays statusof last CI runs per branch."""
    args = ["run", "list", "--limit", str(limit), "--json", "databaseId,headBranch,status,conclusion"]
    if repo:
        args += ["--repo", repo]
    
    data = gh_json(*args)
    display_run_status(data)

# ----- AI FEATURES -----

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
