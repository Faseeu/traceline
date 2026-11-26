# ADR 0002: NetworkX in-memory graph, Qdrant and BM25 for chunks

## Status

Accepted

## Context

The graph layer holds entities and relations extracted from documents. Its size is expected to stay modest for the foreseeable future, and it needs graph algorithms (neighbourhoods, paths). The chunk layer needs semantic search and keyword search over potentially larger text.

## Decision

- The graph is a NetworkX graph held in memory.
- Chunks are stored with vectors in Qdrant for semantic search and indexed with BM25 (`rank-bm25`) for keyword search.
- The two layers are linked only by `chunk_id`.

## Consequences

- Graph operations are simple and need no extra service. The graph must be rebuilt or persisted explicitly, since it is not stored in a database.
- Scaling the graph beyond memory would require a new decision; the in-memory choice is not final for very large corpora.
- Qdrant runs as a separate service (see `docker-compose.yml`), so local development requires Docker.
- BM25 is in-process and rebuilt from chunk text, which is simple but must be kept consistent with Qdrant.
