# discovery.md

## GitHub CLI — explorer vos dépôts

### `gh repo list --limit 10`
Cette commande affiche les 10 premiers dépôts associés au compte GitHub authentifié. Le résultat contient les noms des dépôts, leur visibilité, leurs descriptions ainsi que leur statut public ou privé, ce qui permet d’avoir rapidement une vue d’ensemble des projets disponibles.

### `gh issue list --repo cli/cli`
La commande retourne la liste des issues ouvertes du dépôt `cli/cli`. Chaque ligne affiche le numéro de l’issue, son titre, ses labels et son état actuel, ce qui permet de voir rapidement les bugs, demandes de fonctionnalités et discussions en cours.

### `gh pr list --repo cli/cli --state open`
Cette commande affiche les pull requests ouvertes du dépôt GitHub CLI. Le résultat inclut les numéros des PR, leurs titres, les auteurs et les dates de mise à jour, offrant une vue concise des contributions encore en attente de validation.

---

## Copilot CLI — suggestions de commandes IA

### `gh copilot suggest 'find all python files modified in the last week'`
Copilot a proposé une commande shell utilisant `find` avec des filtres
sur les fichiers `.py` et leur date de modification.
Cela montre comment Copilot peut transformer une demande en langage 
naturel en une commande terminal fonctionnelle.

### `gh copilot explain 'find . -name *.py -mtime -7 -exec wc -l {} +'`
L’explication détaille chaque partie de la commande étape par étape.
Elle précise que la commande recherche les fichiers Python modifiés durant les 7 derniers jours puis compte le nombre de lignes de chaque 
fichier avec `wc -l`.

---

## bat — une meilleure version de cat

### `bat --list-themes`
Cette commande affiche tous les thèmes de coloration syntaxique disponibles dans `bat`. 
Le résultat montre plusieurs thèmes adaptés aux terminaux sombres et clairs.

### `bat --theme=GitHub README.md`
Le fichier README est affiché avec coloration syntaxique et numéros de ligne en utilisant le thème GitHub. Comparé à la commande `cat`, le rendu est beaucoup plus lisible et mieux organisé visuellement.

---

## delta — meilleurs diffs Git

### `git diff HEAD~1 | delta`
Cette commande permet de comparer l'état actuel du dépôt et le commit précédent. 
Le diff Git est affiché avec une mise en forme améliorée , une coloration syntaxique et une meilleure séparation des changements.
Les modifications sont plus faciles à repérer qu’avec l’affichage Git standard.

---

## fzf — recherche floue interactive

### `ls | fzf`
Cette commande ouvre une interface interactive permettant de rechercher rapidement parmi les fichiers du dossier courant. En tapant quelques lettres, la liste est filtrée instantanément.

### `git log --oneline | fzf`
Cette commande permet de rechercher de manière interactive dans l’historique Git.
Elle est utile pour retrouver rapidement un commit grâce à une partie de son message ou de son identifiant.

---

## Gemini CLI

### `gemini 'Explain what a Makefile does in 3 sentences'`
Gemini a généré une explication courte décrivant le rôle d’un Makefile dans l’automatisation des tâches de compilation et d’exécution. La réponse était concise, claire et proche d’une interaction avec un assistant IA.

---

## Claude Code

### `claude 'Summarize the purpose of this repository'`
Claude a analysé le contenu du dépôt puis généré un résumé expliquant l’objectif général et la structure du projet. Cela permet de comprendre rapidement un dépôt inconnu sans devoir lire tous les fichiers manuellement.
