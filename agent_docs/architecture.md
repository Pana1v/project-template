# Architecture

| Path | Job |
|---|---|
| `src/project_template/cli.py` | Typer CLI, one function per command |
| `tests/` | pytest; `test_<module>.py` per module |
| `dashboard/backend/app.py` | FastAPI: `/api/runs`, `/ws/<run>`, serves `frontend/dist` |
| `dashboard/frontend/src/` | React + uPlot, one chart per metric |
| `docker/` | image + compose; build context is the repo root |
| `docs/` | mkdocs-material site for humans |

Data flow: a job writes `logs/<run>/metrics.jsonl` (one JSON object per line, `step` key
for x). The dashboard only reads that file; it never talks to the job directly.

Add a row when you add a module. Remove rows for parts that were dropped.
