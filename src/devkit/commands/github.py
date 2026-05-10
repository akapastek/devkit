import typer
from typing import Annotated

from devkit.config import ConfigTyper
from devkit.utils.gh import gh_json, gh
from devkit.utils.shell import exec_check, CalledProcessError
from devkit.utils.fzf import fzf_select
from devkit.utils.display import (
    rich_print, display_issues, display_pr_summary, display_run_status
)
from devkit.utils.validation import rich_error

# ----- GLOBAL VARS -----

app = ConfigTyper()

# ----- COMMANDS -----

@app.command()
def issues(
    limit: Annotated[int, typer.Option(help='Max number of issues displayed.')] = 10,
    repo: Annotated[str | None, typer.Option(help='Targeted repository.')] = None,
    interactive: Annotated[bool, typer.Option('--interactive', '-i', help='Pipes results through fzf.')] = False
):
    '''List issues as a rich table, colored by state.'''
    # data = gh_json('issue', 'list', '--json', 'title,author,createdAt,state', pretty=True)
    # print(data)
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    if repo is None:
        repo = app.default_repo
    if repo is not None:
        args += ['--repo', repo]
    
    if interactive:
        lines = [f"#{i['number']} {i['title']}" for i in data]
        selected = fzf_select(lines, prompt='Issue > ')
        issue_num = selected.split()[0].lstrip('#')
        gh('issue', 'view', issue_num, '--web') # open in browser
    else:
        data = gh_json(*args)
        display_issues(data, app.get_style())

@app.command()
def pr_summary(
    pr_number: Annotated[int, typer.Argument(..., help='Pull request #.')],
    repo: Annotated[str | None, typer.Option(help='Targeted repository.')] = None
):
    """Display title, body and modified files of a PR."""
    args = ["pr", "view", str(pr_number), "--json", "title,body,files"]
    if repo is None:
        repo = app.default_repo
    if repo is not None:
        args += ["--repo", repo]
    
    data = gh_json(*args)
    display_pr_summary(data, app.get_style())

@app.command()
def start_feature(
    branch_name: Annotated[str, typer.Argument(..., help='New feature\'s branch name.')],
    repo: Annotated[str, typer.Argument(..., help='Targeted repository.')]
):
    """Fork repo and create a branch for the new feature."""
    gh("repo", "fork", repo, "--clone")

    exec_check(["git", "checkout", "-b", branch_name])
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
    if repo is None:
        repo = app.default_repo
    if repo is not None:
        args += ["--repo", repo]
    
    try:
        result = gh(*args)
        rich_print(f"✅ PR created : {result}")
    except CalledProcessError as e:
        rich_error(f"❌ Error : {e.stderr.decode().strip()}")
        raise typer.Exit(1)

@app.command()
def run_status(
    limit: Annotated[int, typer.Option(help='Max number of issues displayed.')] = 10,
    repo: Annotated[str | None, typer.Option(help="Targeted repository.")] = None
):
    """Displays statusof last CI runs per branch."""
    args = ["run", "list", "--limit", str(limit), "--json", "databaseId,headBranch,status,conclusion"]
    if repo is None:
        repo = app.default_repo
    if repo:
        args += ["--repo", repo]
    
    data = gh_json(*args)
    display_run_status(data, app.get_style())
