# Conventions

## Code
- Python 3.12, formatted and linted by ruff (`make fmt`). Line length 110.
- Prefer the standard library and installed deps over new ones.
- Comments say why, not what. A known limit gets `# shortcut: <limit>, <when to upgrade>`.

## Tests
- One focused test per risky piece of logic; it must fail when the logic breaks.
- No network and no GPU in `make test`.

## Commits
```
Short imperative title

Problem: what was wrong or missing.
Outcome: what is true now.
Implementation:
- the main changes, one line each
```
