# Architecture

## Two-layer idea

traceline stores knowledge in two layers that are linked by `chunk_id`:

1. **Chunk layer** — the source text split into chunks. Each chunk has a vector in Qdrant and an entry in an in-memory BM25 index. Chunks are what gets retrieved and quoted.
2. **Graph layer** — a NetworkX graph of entities and relations extracted from chunks. Every node and edge carries the `chunk_id`s it was extracted from, so any graph fact can be traced back to exact source text.

Neither layer stores the other's payload. The graph never copies chunk text, and chunks never embed graph structure. The `chunk_id` is the only join key.

## Layer and dependency rules

- `src/traceline/` is the core library. It contains no UI code and imports no UI frameworks.
- `interfaces/` (CLI, Streamlit, visualisation) is the only layer allowed to import UI packages such as `streamlit` and `pyvis`. This is enforced by ruff rule TID251 in `pyproject.toml`, with a per-file ignore for `interfaces/**`.
- Interfaces depend on the core only through the facade. They never import internal core modules directly.
- Core modules may depend on each other within the package but must not depend on `interfaces/`.
- External services (Groq, Qdrant) are reached only from the core layer. Their use is covered by `integration`-marked tests.

## Target directory tree

Each entry is created in the phase that first needs it. Nothing is created ahead of time.

```
traceline/
├── src/traceline/
│   ├── __init__.py          # Phase 0
│   ├── py.typed             # Phase 0
│   ├── config.py            # created per phase
│   ├── schemas.py           # created per phase
│   └── pipeline.py          # created per phase
├── interfaces/              # created per phase
│   ├── cli.py               # created per phase
│   └── ...                  # created per phase
├── main.py                  # created per phase
├── tests/                   # Phase 0 (test_smoke.py); grows per phase
├── docs/
│   ├── architecture.md      # Phase 0
│   └── adr/                 # Phase 0
└── data/                    # created per phase (git-ignored contents)
```

## Facade

The core exposes three facade methods. Interfaces call only these:

1. `ingest(source)` — read documents, chunk them, and build both layers.
2. `query(question)` — retrieve chunks and graph facts relevant to a question and return an answer with its chunk citations.
3. `trace(entity)` — return the graph neighbourhood of an entity, each fact linked to its source chunks.

The method signatures are defined in the phase that implements them.
