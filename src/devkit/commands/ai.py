import subprocess

# ----- FUNCTIONS -----

class Copilot:
    @staticmethod
    def explain(command: str) -> str:
        '''Ask Copilot CLI to explain a shell command.'''
        prompt = f"The following text between brackets is supposed to be a shell command. You must do the following:\n \
            1) Validity check: Check if the command is valid. If it is, write exactly 'OK', otherwise explain why it's invalid and how to fix.\n \
            2) What it does: Explain what the command does. Include details on each part and add at least one use case example.\n \
            Make sure to output an answer following this exact template: '1) Validity check: ... \\n\\n2) What it does: ...'.\n \
            Pretty print and don't refrain from skipping lines.\
            Here is the text: [{command}]"
        
        result = subprocess.run(
            ['gh', 'copilot', '-p', prompt],
            capture_output=True, text=True
        )
        return result.stdout

    @staticmethod
    def suggest(task: str) -> str:
        '''Ask Copilot CLI to suggest a command to realize the given task.'''
        prompt = f'Answer in the form of a shell command the realization of the task described by the following user input: [{task}]'
        
        result = subprocess.run(
            ['gh', 'copilot', '-p', prompt],
            capture_output=True, text=True
        )
        return result.stdout

class Gemini:
    @staticmethod
    def review(pr_title: str, diff: str) -> str:
        '''AI-powered code review of a pull request.'''
        prompt = f'Review this PR titled "{pr_title}":\n\n{diff[:4000]}'

        result = subprocess.run(
            ['gemini', '-p', prompt],
            capture_output=True, text=True
        )
        return result.stdout

class Mistral:
    @staticmethod
    def commit(diff: str) -> str:
        '''Generate a commit message from staged changes using AI.'''
        prompt = f'Write a conventional commit message for these staged changes:\n\n{diff[:3000]}'
        result = subprocess.run(['vibe', '-p', prompt], capture_output=True, text=True)
        return result.stdout.strip()
