# One entry point for everything. Run `make` for the list.
#
# Blocks between `# >>> <part>` and `# <<< <part>` belong to an optional part;
# `make drop-<part>` deletes them in every file along with the part's folders.

PORT ?= 8080
NAME ?=
PKG   = $(subst -,_,$(NAME))
DOCS := uvx --with mkdocs-material mkdocs

.DEFAULT_GOAL := help
.PHONY: help sync test lint fmt demo docs docs-build rename

help:  ## show this help
	@awk 'BEGIN{FS=":.*## "} /^[a-zA-Z_%-]+:.*## /{printf "  \033[36m%-16s\033[0m %s\n",$$1,$$2}' $(MAKEFILE_LIST)

sync:  ## install / update the python env
	uv sync --all-extras

test:  ## run the tests
	uv run pytest -q

lint:  ## check style and common bugs
	uv run ruff check .
	uv run ruff format --check .

fmt:  ## auto-format and auto-fix
	uv run ruff format .
	uv run ruff check --fix .

demo:  ## write a fake run to logs/ (feeds the dashboard)
	uv run project-template demo

docs:  ## serve the docs with live reload on :8000
	$(DOCS) serve

docs-build:  ## build the docs into site/, fail on warnings
	$(DOCS) build --strict

rename:  ## one-time after "Use this template": make rename NAME=my-tool
	@test -n "$(NAME)" || { echo "usage: make rename NAME=my-tool"; exit 1; }
	git grep -lzI -e project_template -e project-template | xargs -0 sed -i -e 's/project_template/$(PKG)/g' -e 's/project-template/$(NAME)/g'
	git mv src/project_template src/$(PKG)
	git rm -qf --ignore-unmatch .github/workflows/template.yml
	uv lock

drop-%:  ## remove an optional part: drop-dashboard, drop-docker
	@test -n "$(DROP_$*)" || { echo "make: no optional part '$*'"; exit 1; }
	git rm -rqf $(DROP_$*)
	git grep -lz '>>> $*$$' | xargs -0 -r sed -i '/>>> $*$$/,/<<< $*$$/d'
	uv lock

# >>> dashboard
DROP_dashboard := dashboard docs/dashboard.md tests/test_dashboard.py
FRONTEND := dashboard/frontend
.PHONY: frontend dash dash-dev

frontend:  ## build the dashboard frontend into dashboard/frontend/dist
	npm --prefix $(FRONTEND) ci
	npm --prefix $(FRONTEND) run build

dash:  ## serve the dashboard on :$(PORT) (run `make frontend` first)
	uv run --extra dashboard python -m dashboard.backend --port $(PORT)

dash-dev:  ## dashboard with hot reload: backend :$(PORT), Vite :5173
	uv run --extra dashboard python -m dashboard.backend --port $(PORT) & \
	  DASH_BACKEND=http://127.0.0.1:$(PORT) npm --prefix $(FRONTEND) run dev; kill $$!
# <<< dashboard

# >>> docker
DROP_docker := docker
COMPOSE := UID=$$(id -u) GID=$$(id -g) docker compose -f docker/compose.yaml
.PHONY: docker-build up down

docker-build:  ## build the image
	$(COMPOSE) build

up:  ## start the stack in the background
	mkdir -p logs  # else docker creates it as root and the container cannot write
	$(COMPOSE) up -d

down:  ## stop the stack
	$(COMPOSE) down
# <<< docker
