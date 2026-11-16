"""Command line entry point. Add one function per command."""

import json
import math
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from project_template import __version__
from project_template.config import load_config

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
    config: Path = Path("configs/demo.toml"),
    set_: Annotated[
        list[str] | None, typer.Option("--set", help="override a config value: key=value")
    ] = None,
    logs: Path = Path("logs"),
) -> None:
    """Write a fake run to logs/<run>/metrics.jsonl, one JSON line per step.

    The dashboard reads this format; replace with your real job and keep the file format.
    """
    cfg = load_config(config, set_ or [])
    run = logs / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    run.mkdir(parents=True)
    # The run records the config that produced it.
    (run / "config.json").write_text(json.dumps(cfg, indent=2, default=str))
    with open(run / "metrics.jsonl", "w") as f:
        for step in range(cfg["steps"]):
            loss = math.exp(-step / 50) + random.gauss(0, 0.02)
            f.write(json.dumps({"step": step, "loss": loss, "score": 1 - loss}) + "\n")
            f.flush()  # the dashboard tails this file live
            time.sleep(cfg["delay"])
    typer.echo(run)
