import json

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from dashboard.backend.app import create_app


def test_runs_and_stream(tmp_path):
    (tmp_path / "r1").mkdir()
    (tmp_path / "r1" / "metrics.jsonl").write_text(json.dumps({"step": 0, "loss": 1.0}) + "\n")
    client = TestClient(create_app(tmp_path, dist=tmp_path / "none"))

    assert client.get("/api/runs").json() == ["r1"]
    with client.websocket_connect("/ws/r1") as ws:
        assert ws.receive_json() == [{"step": 0, "loss": 1.0}]


def test_stream_skips_bad_lines(tmp_path):
    (tmp_path / "r1").mkdir()
    (tmp_path / "r1" / "metrics.jsonl").write_text('{"step":0}\nnot json\n{"step":1}\n')
    client = TestClient(create_app(tmp_path, dist=tmp_path / "none"))
    with client.websocket_connect("/ws/r1") as ws:
        assert ws.receive_json() == [{"step": 0}, {"step": 1}]


def test_stream_rejects_path_escape(tmp_path):
    (tmp_path / "metrics.jsonl").write_text("{}\n")  # would be served if ".." escaped logs/
    (tmp_path / "logs").mkdir()
    client = TestClient(create_app(tmp_path / "logs", dist=tmp_path / "none"))
    with pytest.raises(WebSocketDisconnect), client.websocket_connect("/ws/%2E%2E") as ws:
        ws.receive_json()
