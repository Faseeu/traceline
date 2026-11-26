# ADR 0001: Library core with thin interfaces

## Status

Accepted

## Context

traceline needs to be used from a CLI, a Streamlit app, and possibly other programs. Mixing UI code into the retrieval logic would make the core hard to test and would tie it to one front end.

## Decision

- The retrieval logic is a Python library in `src/traceline/` using the src layout.
- The core contains no UI code. UI frameworks (`streamlit`, `pyvis`) are banned in the core by ruff TID251.
- All UI lives in `interfaces/` and calls the core through a small facade.

## Consequences

- The core can be tested without a UI, and the same logic serves every interface.
- Interfaces must go through the facade, which adds a small layer of indirection.
- Enforcing the rule with a lint check means a UI import in the core fails CI instead of relying on review.
