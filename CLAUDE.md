# project-template: notes for coding agents

Read `agent_docs/README.md` first; it says which file covers what.

## Commands
- `make sync` install, `make test` tests, `make lint` style, `make docs-build` docs.
- Run `make lint test` before you say a change is done.

## Rules
- Smallest change that fully solves the task. No options or layers nobody asked for.
- New logic with a branch, a parser or a data write gets one test in `tests/`.
- Update `docs/` when a command, file format or route changes.
- Commits: Problem / Outcome / Implementation (see `agent_docs/conventions.md`).
