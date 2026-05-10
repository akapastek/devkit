# config.py
import json
import typer
from pathlib import Path
from rich.progress import Progress

from devkit.utils.shell import exec_capture
from devkit.utils.display import print_panel, create_progress
from devkit.config import load_config, save_config

# ----- GLOBAL VERS -----

CONFIG_FILE = Path.home() / '.devkit' / 'config.json'
DEFAULTS = {
    'ai_tool': 'mistral', # or 'gemini' or 'gh copilot'
    'default_repo': '',
    'theme': 'dark',
    'show_spinner': True,
}

# ----- CLASSES -----

class ConfigTyper(typer.Typer):
    def __init__(self):
        super().__init__()

        self.cfg = load_config()

        # show spinner
        self.progress: Progress | None = None
        if self.cfg.get("show_spinner", default=False):
            self.progress = create_progress()
            self.progress.start()
        self.progress_task = self.progress.add_task('Thinking...')
        
        # default repo
        self.default_repo: str | None = self.cfg.get("default_repo", default=None)
        if self.default_repo == '':
            self.default_repo = None
        
        # ai tool
        ai_tool: str | None = self.cfg.get("ai_tool", default=None)
        assert ai_tool in ["mistral", "gh copilot", "gemini"]
        self.ai_tool: str = ai_tool

        # theme
        self.theme = self.cfg.get("theme", default="light")
        assert self.theme in ["light", "dark"]
    
    def update_progress(self, description: str):
        if self.progress is None:
            return
        self.progress.update(self.progress_task, description=description)

    def stop_progress(self):
        if self.progress is None:
            return
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
    
    # override
    def command(self):
        super().command()
        self.stop_progress()
        save_config(self.cfg)

# ----- FUNCTIONS -----

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return {**DEFAULTS, **json.loads(CONFIG_FILE.read_text())}
    return DEFAULTS

def save_config(cfg: dict):
    CONFIG_FILE.parent.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
