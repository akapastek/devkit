'''Contains all the devkit commands.'''

import typer
import subprocess
from typing import Annotated
from rich.console import Console

# Importation des utilitaires et commandes
from utils.gh import gh_json, gh
from commands.ai import Copilot, Gemini, Mistral
from utils.display import (
    rich_print, print_panel, create_progress,
    display_issues, display_pr_summary, display_run_status
)
from utils.validation import confirm
from utils.check import check_tools  # Ajouté pour le Step 15

# ----- GLOBAL VARS -----

console = Console()
app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """AI-powered developer toolkit"""
    check_tools()  # Vérification de gh, fzf, bat, delta 
    if ctx.invoked_subcommand is None:
        from rich.panel import Panel
        console.print(Panel('Welcome to [bold cyan]devkit[/bold cyan]', border_style='cyan'))
# ----- NON-AI FEATURES -----

@app.command()
def issues(
    limit: Annotated[int, typer.Option(help='Max number of issues displayed.')] = 10,
    repo: Annotated[str | None, typer.Option(help='Targeted repository.')] = None
):
    '''List issues as a rich table, colored by state.'''
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    if repo is not None:
        args += ['--repo', repo]
    
    data = gh_json(*args)
    display_issues(data)

@app.command()
def pr_summary(
    pr_number: Annotated[int, typer.Argument(help='Pull request #.')] = ...,
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
    branch_name: Annotated[str, typer.Argument(help="New feature's branch name.")] = ...,
    repo: Annotated[str, typer.Argument(help="Targeted repository.")] = ...
):
    """Fork repo and create a branch for the new feature."""
    """Fork le repo et crée une branche (Step 12/15)."""
    try:
        # On tente le fork et le clone
        gh("repo", "fork", repo, "--clone")
    except Exception:
        # Si ça échoue (ex: dossier déjà présent), on affiche un message simple et on continue
        rich_print("[yellow]Le dépôt est déjà présent ou le fork existe déjà. Passage à la création de branche...[/yellow]")

    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    rich_print(f"✅ Branch '{branch_name}' created and ready for the feature !")

@app.command()
def open_pr(
    title: Annotated[str, typer.Argument(help="PR title.")] = ...,
    base: Annotated[str, typer.Argument(help="Base branch (ex: main).")] = "main",
    head: Annotated[str, typer.Argument(help="Source branch.")] = ...,
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
        rich_print(f"❌ Error : {e.stderr}", err=True)
        raise typer.Exit(1)

@app.command()
def run_status(
    limit: Annotated[int, typer.Option(help='Max number of runs.')] = 10,
    repo: Annotated[str | None, typer.Option(help="Targeted repository.")] = None
):
    """Displays status of last CI runs per branch."""
    args = ["run", "list", "--limit", str(limit), "--json", "databaseId,headBranch,status,conclusion"]
    if repo:
        args += ["--repo", repo]
    
    data = gh_json(*args)
    display_run_status(data)

# ----- AI FEATURES -----

@app.command()
def explain(command: Annotated[str, typer.Argument(help='Shell command to explain')] = ...):
    '''Ask Copilot CLI to explain a shell command.'''
    result_text = Copilot.explain(command)
    print_panel('[purple]Copilot Explanation[/purple]', result_text)

@app.command()
def suggest(command: Annotated[str, typer.Argument(help='Task to accomplish')] = ...):
    '''Ask Copilot CLI to suggest a command.'''
    result_text = Copilot.suggest(command)
    print_panel('[purple]Copilot Suggestion[/purple]', result_text)

@app.command()
def review(
    pr_number: Annotated[int, typer.Argument(help='PR number to review')] = ...,
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

    if confirm('Use this message?'):
        subprocess.run(['git', 'commit', '-m', suggested])

# ----- MAIN -----

if __name__ == '__main__':
    app()
