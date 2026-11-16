# CLI

The CLI is a [Typer](https://typer.tiangolo.com/) app in `src/project_template/cli.py`.
Each command is one function; its docstring is the help text.

| Command | What it does |
|---|---|
| `project-template version` | print the installed version |
| `project-template hello --name X` | placeholder, replace with the first real command |
| `project-template demo --set steps=50` | write a fake run to `logs/<run>/metrics.jsonl`, settings from `configs/demo.toml` |

`uv run project-template <command> --help` shows the options of one command.

## Configs

Jobs read TOML files from `configs/` with `config.load_config(path, overrides)`:

- `base = "other.toml"` at the top inherits that file; tables merge key by key.
- `--set opt.lr=3e-4` overrides one existing value (a typo in the key is an error); the value is parsed as TOML, a bare word stays a string.
- Each run writes the final config to `logs/<run>/config.json`.
