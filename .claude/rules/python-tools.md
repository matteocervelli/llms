---
paths:
  - "**/*.py"
  - "pyproject.toml"
  - "requirements*.txt"
  - "setup.py"
  - "setup.cfg"
---

# Python Tools Rules

Always use `uv` for Python operations. Never use bare `python`, `pip`, or `venv`.

- Run: `uv run python script.py`, `uv run pytest`, `uv run mypy .`
- Install: `uv add requests`, `uv add --dev pytest`
- Setup: `uv init`, `uv venv`, `uv sync`

Why: 10-100x faster than pip, consistent lockfiles, no activation scripts needed.
