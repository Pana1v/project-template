"""FastAPI app: run list over REST, live metrics over WebSocket, built frontend on /."""

import asyncio
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

DIST = Path(__file__).resolve().parents[1] / "frontend" / "dist"
POLL_S = 0.5


def create_app(logs: Path = Path("logs"), dist: Path = DIST) -> FastAPI:
    logs = logs.resolve()
    app = FastAPI(title="project-template dashboard")

    def metrics_file(run: str) -> Path:
        path = (logs / run / "metrics.jsonl").resolve()
        if path.parent.parent != logs or not path.is_file():  # blocks ../ and nested paths
            raise HTTPException(404, f"no run {run!r}")
        return path

    @app.get("/api/runs")
    def runs() -> list[str]:
        """Run ids, newest first."""
        files = sorted(logs.glob("*/metrics.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        return [p.parent.name for p in files]

    @app.websocket("/ws/{run}")
    async def stream(ws: WebSocket, run: str):
        """Send every metrics row of the run, then keep sending rows as they are appended."""
        try:
            path = metrics_file(run)
        except HTTPException:
            await ws.close(code=4404)
            return
        await ws.accept()
        try:
            with open(path) as f:  # noqa: ASYNC230 small local appends, a read never blocks for long
                buf = ""
                while True:
                    buf += f.read()
                    *lines, buf = buf.split("\n")  # keep a half-written last line for the next read
                    rows = []
                    for x in lines:
                        try:
                            rows.append(json.loads(x))
                        except json.JSONDecodeError:
                            pass  # blank or corrupt line: skip it, keep the stream alive
                    if rows:
                        await ws.send_json(rows)
                    await asyncio.sleep(POLL_S)
        except WebSocketDisconnect:
            pass

    if dist.is_dir():
        app.mount("/", StaticFiles(directory=dist, html=True), name="frontend")
    return app
