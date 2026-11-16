# Build context is the repo root: docker compose -f docker/compose.yaml build
# >>> dashboard
FROM node:26-slim AS frontend
WORKDIR /src
COPY dashboard/frontend/package*.json ./
RUN npm ci
COPY dashboard/frontend ./
RUN npm run build
# <<< dashboard

FROM python:3.15-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PATH=/app/.venv/bin:$PATH
# Dependencies first so code edits do not reinstall them.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --all-extras --no-install-project
COPY . .
RUN uv sync --frozen --no-dev --all-extras
# >>> dashboard
COPY --from=frontend /src/dist dashboard/frontend/dist
# <<< dashboard
ENTRYPOINT ["project-template"]
CMD ["--help"]
