# Devkit
AI-powered developer toolkit.

Authors :
- DIAGNE Abdoul
- ALBERT Kendal

## Install

In the project's root directory, run this:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

## Help

Inside your virtual environment, run this:

```sh
devkit                  # to list groups
devkit [GROUP] --help   # to list GROUP's commands
```

## Use

Inside your virtual environment, run this:

## Configuration

In your user directory, edit the file `.devkit/config.json`.
This file should be created automatically after you execute one command from devkit.

`config.json` example :
```json
{
  "ai_tool": "copilot",
  "default_repo": null,
  "theme": "dark",
  "show_spinner": true
}
```

```sh
devkit [GROUP] [COMMAND] [ARGUMENTS]... [OPTIONS]...
```

## Live Demo (recorded with asciinema)
[![devkitdemo](https://asciinema.org/a/RrC9WPNb6XP5CogJ.svg)](https://asciinema.org/a/RrC9WPNb6XP5CogJ)
