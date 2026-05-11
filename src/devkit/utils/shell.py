import subprocess

# ----- GLOBAL VARS -----

CalledProcessError = subprocess.CalledProcessError

# ----- FUNCTIONS -----

def exec_check(command: list[str]):
    subprocess.run(command, check=True)

def exec_capture(command: list[str], *, input: str = '') -> str:
    return subprocess.run(
        command,
        capture_output=True, text=True, check=True,
        input=input
    ).stdout.strip()
