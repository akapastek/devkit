import typer

from devkit.utils.gh import gh, gh_json
from devkit.utils.shell import exec_check
from devkit.utils.display import rich_print, print_panel, rich_rule
from devkit.commands.ai import mistral_scaffold

# ----- GLOBAL VARS -----

app = typer.Typer()

# ----- COMMANDS

@app.command('feature-start')
def feature_start(
    name: str = typer.Argument(..., help='Feature name (kebab-case)'),
    issue: int = typer.Option(None, help='Issue number to link'),
):
    '''Start a new feature: branch + draft PR + AI scaffold.'''

    rich_rule('[bold]Starting Feature[/bold]')

    # 1. Create branch
    branch = f'feature/{name}'
    exec_check(['git', 'checkout', '-b', branch])
    rich_print(f'[green] [/green] Created branch: {branch}')

    # 2. Push branch
    exec_check(['git', 'push', '-u', 'origin', branch])

    # 3. Create draft PR
    pr_title = name.replace('-', ' ').title()
    pr_args = ['pr', 'create', '--draft', '--title', pr_title, '--body', '']
    if issue:
        pr_args += ['--body', f'Closes #{issue}']
    pr_url = gh(*pr_args)
    rich_print(f'[green] [/green] Draft PR: {pr_url}')

    # 4. AI scaffold
    if issue:
        issue_body = gh_json('issue', 'view', str(issue), '--json',
        'title,body')
        plan_stdout = mistral_scaffold(issue_body)
        print_panel(plan_stdout, title='[cyan]AI Implementation Plan[/cyan]', border_style='cyan')

    rich_rule('[green]Ready to code![/green]')
