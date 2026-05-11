import shutil
from rich.console import Console
console = Console(stderr=True)
REQUIRED_TOOLS = {
  'gh': 'Install from https://cli.github.com',
  'fzf': 'brew install fzf or apt install fzf',
  'bat': 'brew install bat or apt install bat',
  'delta': 'brew install git-delta',
}
def check_tools():
   missing = {t: hint for t, hint in REQUIRED_TOOLS.items() if not 
shutil.which(t)}
   if missing:
      console.print('[red]Missing required tools:[/red]')
      for tool, hint in missing.items():
         console.print(f' [cyan]{tool}[/cyan] — {hint}')
      raise SystemExit(1)

