# CLI

The CLI is a [Typer](https://typer.tiangolo.com/) app in `src/project_template/cli.py`.
Each command is one function; its docstring is the help text.

| Command | What it does |
|---|---|
| `project-template version` | print the installed version |
| `project-template hello --name X` | placeholder, replace with the first real command |
| `project-template demo` | write a fake run to `logs/<run>/metrics.jsonl` |

`uv run project-template <command> --help` shows the options of one command.
