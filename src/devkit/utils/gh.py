import json
from typing import Any

from devkit.utils.shell import exec_capture

# ----- FUNCTIONS -----

def gh(*args: str) -> str:
    '''Run a gh command and return stdout as string.'''
    result = exec_capture(['gh', *args])
    return result.strip()

def gh_json(*args: str, pretty: bool = False) -> Any:
    '''Run a gh command with --json and parse result.'''
    raw = gh(*args)
    
    data = json.loads(raw) if raw else []
    return json.dumps(data, indent=4) if pretty else data
