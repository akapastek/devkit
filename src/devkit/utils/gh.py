import subprocess
import json
from typing import Any

# ----- FUNCTIONS -----

def gh(*args: str) -> str:
    '''Run a gh command and return stdout as string.'''
    result = subprocess.run(
        ['gh', *args],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def gh_json(*args: str, pretty: bool = False) -> Any:
    '''Run a gh command with --json and parse result.'''
    raw = gh(*args)
    
    data = json.loads(raw) if raw else []
    return json.dumps(data, indent=4) if pretty else data
