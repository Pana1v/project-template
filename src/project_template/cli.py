"""Command line entry point. Add one function per command."""

import json
import math
import random
import time
from datetime import datetime
from pathlib import Path

import typer

from project_template import __version__

app = typer.Typer(no_args_is_help=True, help="project-template command line.")


@app.command()
def version() -> None:
    """Print the installed version."""
    typer.echo(__version__)


@app.command()
def hello(name: str = "world") -> None:
    """Say hello. Replace with your first real command."""
    typer.echo(f"hello {name}")


@app.command()
def demo(
    steps: int = typer.Option(200, min=1),
    delay: float = typer.Option(0.05, min=0.0, help="seconds between steps"),
    logs: Path = Path("logs"),
) -> None:
    """Write a fake run to logs/<run>/metrics.jsonl, one JSON line per step.

    The dashboard reads this format; replace with your real job and keep the file format.
    """
    run = logs / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run.mkdir(parents=True)
    with open(run / "metrics.jsonl", "w") as f:
        for step in range(steps):
            loss = math.exp(-step / 50) + random.gauss(0, 0.02)
            f.write(json.dumps({"step": step, "loss": loss, "score": 1 - loss}) + "\n")
            f.flush()  # the dashboard tails this file live
            time.sleep(delay)
    typer.echo(run)
