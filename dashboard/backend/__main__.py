import argparse
from pathlib import Path

import uvicorn

from dashboard.backend.app import create_app

p = argparse.ArgumentParser(description="Serve the dashboard.")
p.add_argument("--host", default="127.0.0.1")
p.add_argument("--port", type=int, default=8080)
p.add_argument("--logs", type=Path, default=Path("logs"))
a = p.parse_args()
uvicorn.run(create_app(a.logs), host=a.host, port=a.port)
