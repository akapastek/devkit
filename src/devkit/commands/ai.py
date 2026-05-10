import typer
from typing import Annotated, Any

from devkit.utils.gh import gh_json, gh
from devkit.utils.shell import exec_capture, exec_check
from devkit.utils.display import rich_print, print_panel, create_progress
from devkit.utils.validation import confirm

# ----- GLOBAL VARS -----

app = typer.Typer()

# ----- FUNCTIONS -----

def copilot_explain(command: str) -> str:
    '''Ask Copilot CLI to explain a shell command.'''
    prompt = f"The following text between brackets is supposed to be a shell command. You must do the following:\n \
        1) Validity check: Check if the command is valid. If it is, write exactly 'OK', otherwise explain why it's invalid and how to fix.\n \
        2) What it does: Explain what the command does. Include details on each part and add at least one use case example.\n \
        Make sure to output an answer following this exact template: '1) Validity check: ... \\n\\n2) What it does: ...'.\n \
        Pretty print and don't refrain from skipping lines.\
        Here is the text: [{command}]"
    
    return exec_capture(['gh', 'copilot', '-p', prompt])

def copilot_suggest(task: str) -> str:
    '''Ask Copilot CLI to suggest a command to realize the given task.'''
    prompt = f'Answer in the form of a shell command the realization of the task described by the following user input: [{task}]'
    
    return exec_capture(['gh', 'copilot', '-p', prompt])

def gemini_review(pr_title: str, diff: str) -> str:
    '''AI-powered code review of a pull request.'''
    prompt = f'Review this PR titled "{pr_title}":\n\n{diff[:4000]}'

    return exec_capture(['gemini', '-p', prompt])

def mistral_commit(diff: str) -> str:
    '''Generate a commit message from staged changes using AI.'''
    prompt = f'Write a conventional commit message for these staged changes:\n\n{diff[:3000]}'
    result = exec_capture(['vibe', '-p', prompt])
    return result.strip()

def mistral_scaffold(issue_body: Any) -> str:
    '''AI scaffold used in `./workflow.py` .'''
    prompt = f'I\'m starting work on: {issue_body["title"]}\n{issue_body["body"]}\nSuggest a step-by-step implementation plan.'
    return exec_capture(['vibe', '-p', prompt])

# ----- COMMANDS -----

@app.command()
def explain(command: Annotated[str, typer.Argument(..., help='Shell command to explain')]):
    '''Ask Copilot CLI to explain a shell command.'''
    result_text = copilot_explain(command)
    print_panel('[purple]Copilot Explaination[/purple]', result_text)

@app.command()
def suggest(command: Annotated[str, typer.Argument(..., help='Task to accomplish')]):
    '''Ask Copilot CLI to suggest a command.'''
    result_text = copilot_suggest(command)
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
        result = gemini_review(pr_info["title"], diff)

    print_panel(f'[cyan]AI Review — PR #{pr_number}[/cyan]', result)

@app.command()
def commit():
    '''Generate a commit message from staged changes using AI.'''
    diff = exec_capture(['git', 'diff', '--cached'], text=True)
    if not diff.strip():
        rich_print('[yellow]No staged changes.[/yellow]')
        raise typer.Exit()
    
    suggested = mistral_commit(diff)
    print_panel('[green]Suggested Commit Message[/green]', suggested)

    confirm('Use this message?')
    exec_check(['git', 'commit', '-m', suggested])
