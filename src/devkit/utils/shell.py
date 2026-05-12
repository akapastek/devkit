'''subprocess util functions.'''

import subprocess

# ----- GLOBAL VARS -----

CalledProcessError = subprocess.CalledProcessError

# ----- FUNCTIONS -----

def exec_check(command: list[str]):
    '''Check subprocess output without capture.'''
    subprocess.run(command, check=True)

def exec_capture(command: list[str], *, input: str = '') -> str:
    '''Check subprocess output with check and capture.'''
    return subprocess.run(
        command,
        capture_output=True, text=True, check=True,
        input=input
    ).stdout.strip()
