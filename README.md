# project-template

Starting point for a new project: Typer CLI, tests, ruff, mkdocs-material docs and agent docs,
plus the optional parts listed under Layout. One `Makefile` drives it all.

## Start a project from it

1. On GitHub: **Use this template**, then clone the new repo.
2. Rename and trim, then commit:
   ```bash
   make rename NAME=my-tool          # package my_tool, command my-tool, everywhere
   make drop-dashboard               # optional: no dashboard
   make drop-docker                  # optional: no Docker
   git commit -am "Start my-tool from project-template"
   ```
3. Fill in `docs/index.md`, `agent_docs/architecture.md` and this README.

## Use

```bash
make                 # list every target
make sync test       # install and test
uv run project-template --help
make docs            # docs on http://localhost:8000
```

[^dashboard-use]: >>> dashboard

```bash
make frontend dash   # dashboard on http://localhost:8080, feed it with `make demo`
```

[^dashboard-use-end]: <<< dashboard

[^docker-use]: >>> docker

```bash
make docker-build up # run it in containers
```

[^docker-use-end]: <<< docker

## Layout

| Path | What |
|---|---|
| `src/project_template/` | the package; `cli.py` is the entry point |
| `tests/` | pytest |
| `docs/`, `mkdocs.yml` | docs site for humans |
| `CLAUDE.md` (= `AGENTS.md`), `agent_docs/` | context for coding agents |

[^dashboard-layout]: >>> dashboard

- `dashboard/`: optional, FastAPI + React live metrics

[^dashboard-layout-end]: <<< dashboard

[^docker-layout]: >>> docker

- `docker/`: optional, image and compose file

[^docker-layout-end]: <<< docker

Optional parts are fenced with `# >>> <part>` / `# <<< <part>` lines in shared files (in
Markdown, as unused footnotes such as `[^x]: >>> <part>`, which GitHub does not render), so
`make drop-<part>` can remove them cleanly.
