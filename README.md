# traceline

traceline is a Python library for retrieval over documents using two linked layers: text chunks for semantic and keyword search, and a knowledge graph of entities and relations that points back to those chunks through a shared `chunk_id`. Answers can be traced from the graph to the exact source text they came from. The core is a library with thin interfaces on top, and it calls Groq for language-model work and Qdrant for vector storage.

## Setup

Install the Python dependencies (Python 3.12 is pinned in `.python-version`):

```bash
uv sync
```

Copy the environment template and fill in your Groq key:

```bash
cp .env.example .env
```

Start Qdrant (and the app container) with Docker:

```bash
docker compose up -d
```

Qdrant is then available at http://localhost:6333.

## Status: Phase 0

Repository bootstrap is in progress. No retrieval features exist yet.

## Architecture

## Usage
