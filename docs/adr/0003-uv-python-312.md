# ADR 0003: uv and Python 3.12

## Status

Accepted

## Context

The project needs a reproducible environment, fast dependency resolution, and a single tool for running commands, locking dependencies, and building images.

## Decision

- Use `uv` for installing Python, managing dependencies (`uv.lock`), and running commands (`uv run`).
- Pin Python 3.12 in `.python-version` and `requires-python` in `pyproject.toml`.
- Docker images use `python:3.12-slim` and `uv sync --frozen --no-dev`.

## Consequences

- Every developer and CI run uses the same interpreter and locked versions.
- Contributors must have uv installed; it does not require a separate virtualenv workflow.
- Upgrading Python later means changing three places (`.python-version`, `requires-python`, and the Docker base image) and regenerating the lock file.
