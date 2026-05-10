import typer
from typing import Annotated, Any

from devkit.config import ConfigTyper
from devkit.utils.gh import gh_json, gh
from devkit.utils.shell import exec_capture, exec_check
from devkit.utils.display import rich_print
from devkit.utils.validation import confirm

# ----- GLOBAL VARS -----

app = ConfigTyper()

# ----- FUNCTIONS -----

def scaffold(issue_body: Any) -> str:
    '''AI scaffold used in `./workflow.py` .'''
    prompt = f'I\'m starting work on: {issue_body["title"]}\n{issue_body["body"]}\nSuggest a step-by-step implementation plan.'
    return app.ai_output(prompt)

# ----- COMMANDS -----

@app.command()
def explain(command: Annotated[str, typer.Argument(..., help='Shell command to explain')]):
    '''Ask AI to explain a shell command.'''
    prompt = f"The following text between brackets is supposed to be a shell command. You must do the following:\n \
        1) Validity check: Check if the command is valid. If it is, write exactly 'OK', otherwise explain why it's invalid and how to fix.\n \
        2) What it does: Explain what the command does. Include details on each part and add at least one use case example.\n \
        Make sure to output an answer following this exact template: '1) Validity check: ... \\n\\n2) What it does: ...'.\n \
        Pretty print and don't refrain from skipping lines.\
        Here is the text: [{command}]"

    app.print_ai_output(prompt, 'Copilot Explaination')

@app.command()
def suggest(command: Annotated[str, typer.Argument(..., help='Task to accomplish')]):
    '''Ask AI to suggest a command to realize the given task.'''
    prompt = f'Answer in the form of a shell command the realization of the task described by the following user input: [{command}]'
    
    app.print_ai_output(prompt, 'Copilot Suggestion')

@app.command()
def review(
    pr_number: Annotated[int, typer.Argument(..., help='PR number to review')],
):
    '''AI-powered code review of a pull request.'''
    app.update_progress('Fetching PR diff...')
    diff = gh('pr', 'diff', str(pr_number))
    pr_info = gh_json('pr', 'view', str(pr_number), '--json', 'title,body')

    app.update_progress('Running AI review...')
    prompt = f'Review this PR titled "{pr_info["title"]}":\n\n{diff[:4000]}'
    app.print_ai_output(prompt, 'AI Review — PR #{pr_number}')

@app.command()
def commit():
    '''Generate a commit message from staged changes using AI.'''
    diff = exec_capture(['git', 'diff', '--cached'], text=True)
    if not diff.strip():
        rich_print('[yellow]No staged changes.[/yellow]')
        raise typer.Exit()
    
    prompt = f'Write a conventional commit message for these staged changes:\n\n{diff[:3000]}'
    suggested = app.ai_output(prompt)
    app.print_with_theme(suggested, 'Suggested Commit Message')

    confirm('Use this message?')
    exec_check(['git', 'commit', '-m', suggested])
