# Contributing

## Development Commands

Formatting / linting (run this before pushing):

```bash
uv run ruff format src/ # Format
uv run ruff check --fix  src/ # Linting with auto fix
uv run pyright src/ # Type checking
```

## CI

This repository comes with a [GitHub Actions Workflow](.github/workflows/lint.yml) that runs formatting and linting
checks on each push to main and each pull request, and is a precondition for merging.

The workflow uses [Ruff](https://docs.astral.sh/ruff/) and [Pyright](https://github.com/microsoft/pyright).

## Proto Dependencies

Generated code is pulled from the [Buf Schema Registry](https://buf.build/beyer-labs/h2pcontrol) via the
`buf.build/gen/python` index configured in `pyproject.toml`. To update to the latest proto versions:

```bash
uv sync --upgrade
```
