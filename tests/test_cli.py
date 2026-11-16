import json

from typer.testing import CliRunner

from project_template import __version__
from project_template.cli import app

runner = CliRunner()


def test_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert r.stdout.strip() == __version__


def test_demo_writes_metrics(tmp_path):
    r = runner.invoke(app, ["demo", "--steps", "3", "--delay", "0", "--logs", str(tmp_path)])
    assert r.exit_code == 0, r.output
    lines = next(tmp_path.glob("*/metrics.jsonl")).read_text().splitlines()
    assert [json.loads(x)["step"] for x in lines] == [0, 1, 2]
