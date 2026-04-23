import subprocess
import json
from typing import Any, List
from rich.console import Console
from rich.table import Table
import typer
from rich import box
app = typer.Typer()
#i'mworking on a new project , it is exciting
def gh(*args: str) -> str:
    result = subprocess.run(['gh', *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def gh_json(*args: str) -> Any:
    raw = gh(*args)
    return json.loads(raw) if raw else []

@app.command()
def issues(repo: str , limit: int):
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    if repo:
        args += ['--repo', repo]
    data = gh_json(*args)
    # Affichage avec rich.Table
    table = Table(title='Open Issues', border_style='green')
    table.add_column('#', style='cyan', width=6)
    table.add_column('Title', min_width=30)
    table.add_column('Labels', width=20)
    for issue in data:
        labels = ', '.join(l['name'] for l in issue.get('labels', []))
        table.add_row(str(issue['number']), issue['title'], labels or '—')
    Console().print(table)

@app.command()
def pr_summary(
    pr_number:int,
    repo: str 
):
    """Affiche le titre, le corps et les fichiers modifiés d'une PR."""
    args = ["pr", "view", str(pr_number), "--json", "title,body,files"]
    if repo:
        args += ["--repo", repo]
    data = gh_json(*args)

    console = Console()
    table = Table(title=f"PR #{pr_number} Summary", border_style="blue", box=box.ROUNDED)
    table.add_column("Title", style="bold magenta", width=50)
    table.add_column("Files Changed", width=30)

    table.add_row(data["title"], str(len(data["files"])) + " files")

    console.print(table)
    console.print("\n[bold]Body:[/bold]\n" + (data["body"] or "—"))

    if data["files"]:
        console.print("\n[bold]Changed Files:[/bold]")
        for f in data["files"]:
            console.print(f"  - {f['path']}")


@app.command()
def start_feature(
    branch_name: str = typer.Argument(..., help="Nom de la branche pour la nouvelle feature"),
    repo: str = typer.Option("", help="Propriétaire/dépôt (ex: owner/repo)"),
):
    """Fork le dépôt et crée une branche pour une nouvelle feature."""
    if repo:
        gh("repo", "fork", repo, "--clone")
    else:
        typer.echo("Erreur : il faut spécifier un dépôt avec --repo", err=True)
        raise typer.Exit(1)

    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    typer.echo(f"✅ Branche '{branch_name}' créée et prête pour la feature !")

@app.command()
@app.command()
def open_pr(
    title: str = typer.Option(..., prompt="Titre de la PR"),
    body: str = typer.Option(..., prompt="Corps de la PR"),
    repo: str = typer.Option(..., help="Propriétaire/dépôt (ex: owner/repo)"),
    base: str = typer.Option("main", help="Branche de base (ex: tests)"),
    head: str = typer.Option(..., help="Branche source (ex: ma-branche)"),
):
    """Crée une PR."""
    args = ["pr", "create", "--title", title, "--body", body, "--fill", "--repo", repo, "--base", base, "--head", head]
    try:
        result = gh(*args)
        typer.echo(f"✅ PR créée : {result}")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Erreur : {e.stderr.decode().strip()}", err=True)
        raise typer.Exit(1)
@app.command()
def run_status(
    repo: str = typer.Option("", help="Propriétaire/dépôt (ex: owner/repo)"),
    limit: int = typer.Option(10, help="Nombre maximum de runs à afficher"),
):
    """Affiche le statut des derniers runs CI par branche."""
    args = ["run", "list", "--limit", str(limit), "--json", "databaseId,headBranch,status,conclusion"]
    if repo:
        args += ["--repo", repo]
    data = gh_json(*args)

    console = Console()
    table = Table(title="CI Run Status", border_style="cyan", box=box.ROUNDED)
    table.add_column("Branch", style="bold blue")
    table.add_column("Status", width=12)
    table.add_column("Conclusion", width=12)

    for run in data:
        status = run["status"]
        conclusion = run["conclusion"]
        color = "yellow" if status == "queued" else "green" if conclusion == "success" else "red"
        table.add_row(
            run["headBranch"],
            f"[{color}]{status}[/{color}]",
            f"[{color}]{conclusion or '—'}[/{color}]",
        )

    console.print(table)

if __name__ == "__main__":
    app()
