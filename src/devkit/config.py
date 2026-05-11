# config.py
import json
import typer
from pathlib import Path
from functools import wraps
from rich.progress import Progress, TaskID

from devkit.utils.shell import exec_capture
from devkit.utils.display import print_panel, create_progress
from devkit.utils.validation import rich_error

# ----- GLOBAL VERS -----

CONFIG_FILE = Path.home() / '.devkit' / 'config.json'
DEFAULTS = {
    'ai_tool': 'mistral', # or 'gemini' or 'gh copilot'
    'default_repo': '',
    'theme': 'light',
    'show_spinner': True,
}

# ----- CLASSES -----

class ConfigTyper(typer.Typer):
    cfg: dict | None = None

    def __init__(self, init_progress_message: str = 'Loading...'):
        super().__init__()

        # load config once
        if ConfigTyper.cfg is None:
            ConfigTyper.cfg = load_config()
            validate_config(ConfigTyper.cfg)
            parse_config(ConfigTyper.cfg)
        self.cfg = ConfigTyper.cfg

        # show spinner
        self.progress: Progress | None = None
        self.progress_task: TaskID | None = None
        if self.cfg.get('show_spinner'):
            self.progress = create_progress()
            self.progress_task = self.progress.add_task(init_progress_message)
        
        # rest
        self.default_repo: str | None = self.cfg['default_repo']
        self.ai_tool: str = self.cfg['ai_tool']
        self.theme: str = self.cfg['theme']
    
    # override
    def command(self, name: str | None = None):
        def wrap_command(decorator):
            '''Handles automatic progress display and saving configuration.'''
            def new_f(f):
                @wraps(f)
                def wrapper(*args, **kwargs):
                    if self.progress is not None:
                        self.progress.start()
                    try:
                        f(*args, **kwargs)
                    finally:
                        self.stop_progress()
                        save_config(self.cfg)
                return decorator(wrapper)
            return new_f

        return wrap_command(super().command(name))
    
    def update_progress(self, description: str):
        if self.progress is None:
            return
        self.progress.update(self.progress_task, description=description)

    def stop_progress(self):
        if self.progress is None:
            return
        self.update_progress("Done.")
        self.progress.stop()
        self.progress = None
    
    def ai_output(self, prompt: str) -> str:
        out = exec_capture([self.ai_tool, '-p', prompt])
        self.stop_progress()
        return out
    
    def get_style(self) -> str:
        return 'cyan' if self.theme == 'light' else 'purple'
    
    def print_with_theme(self, content: str, panel_title: str):
        style = self.get_style()
        panel_title = f'[{style}]{panel_title}[/{style}]'
        print_panel(panel_title, content, border_style=style)

    def print_ai_output(self, prompt: str, panel_title: str):
        out = self.ai_output(prompt)
        self.print_with_theme(out, panel_title)

# ----- FUNCTIONS -----

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return {**DEFAULTS, **json.loads(CONFIG_FILE.read_text())}
    return DEFAULTS

def save_config(cfg: dict):
    # unparse ai tool
    ai_tool_convert = {
        'vibe': 'mistral',
        'gh copilot': 'copilot',
        'gemini': 'gemini'
    }
    cfg["ai_tool"] = ai_tool_convert[cfg["ai_tool"]]

    CONFIG_FILE.parent.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))

def validate_config(cfg: dict):
    '''Verifies configuration has correct format and values.'''
    def aux(key: str, is_in: list[str]):
        val = str(cfg.get(key, None))
        if not val in is_in:
            rich_error(f"[red]Error :[/red] '{val}' is not a valid value for key config '{key}'.\nValid values: {is_in}.")
            exit(1)
    
    to_verify: list[tuple[str, list[str]]] = [
        ("ai_tool", ["mistral", "copilot", "gemini"]),
        ("theme", ["light", "dark", "None"]),
        ("show_spinner", ["False", "True", "None"]),
    ]
    for key, is_in in to_verify:
        aux(key, is_in)

def parse_config(cfg: dict):
    '''Assumes validate_config(cfg) was called before.'''
    # ai tool
    ai_tool_convert = {
        'mistral': 'vibe',
        'copilot': 'gh copilot',
        'gemini': 'gemini'
    }
    cfg["ai_tool"] = ai_tool_convert[cfg["ai_tool"]]

    # default repo
    if cfg.get("default_repo", None) == '':
        cfg["default_repo"] = None

    # theme
    if str(cfg["theme"]) == "None":
        cfg["theme"] = "light"

    # show spinner
    if str(cfg["show_spinner"]) == "None":
        cfg["show_spinner"] = False
