# Dashboard

A FastAPI backend (`dashboard/backend/app.py`) and a Vite + React frontend
(`dashboard/frontend`). The backend lists runs under `logs/` and streams each run's
`metrics.jsonl` over a WebSocket. The frontend draws one chart per numeric key.

```bash
make frontend      # once, and after frontend changes
make dash          # http://localhost:8080
make demo          # in another terminal: a live run to watch
make dash-dev      # hot reload on http://localhost:5173
```

## Feeding it

Write one JSON object per line to `logs/<run>/metrics.jsonl` and flush after each line.
`step` is the x axis; every other numeric key gets its own chart.

| Route | Returns |
|---|---|
| `GET /api/runs` | run ids, newest first |
| `WS /ws/<run>` | all rows so far as a JSON array, then new rows as they are appended |

Not needed: `make drop-dashboard` removes it everywhere.
