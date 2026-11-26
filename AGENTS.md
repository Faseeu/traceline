# AGENTS.md

Guidance for AI coding agents working in this repository.

## Layer rules

- The core library lives in `src/traceline/`. It must not import UI frameworks. `streamlit` and `pyvis` are banned there by ruff rule TID251.
- Interfaces (CLI, Streamlit, graph rendering) live under `interfaces/` and are the only place allowed to import UI code. They call the core through its facade and never reach into internal modules.
- Chunks (text + vectors + BM25 index) and the graph (NetworkX) are linked only by `chunk_id`. Do not duplicate chunk text into graph nodes.
- See `docs/architecture.md` for the full rules and the target layout.

## Working rules

- No empty or placeholder files. Do not create modules, schemas, or folders before the phase that needs them.
- Ask before adding a dependency. Use `uv add` (runtime) or `uv add --dev` (tooling) only after confirmation.
- Every new module ships with tests in `tests/`.
- Tests that call Groq or Qdrant are marked `@pytest.mark.integration` and are excluded by default.
- Python 3.12 only (see `.python-version`). Use `uv` for everything; do not use `pip` directly.

## Commands

- `make install` — `uv sync`
- `make test` — `uv run pytest` (integration tests excluded by default)
- `make lint` — `ruff check` and `ruff format --check`
- `make format` — apply `ruff format` and auto-fixes
- `make up` / `make down` — start / stop Docker services (Qdrant and app)
