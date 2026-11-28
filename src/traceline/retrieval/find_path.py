# src/traceline/retrieval/graph_search.py   (pure functions, no I/O)
def default_cost(edge: Edge) -> float:               # 1 / confidence
    ...

def find_path(
    graph: GraphStore, source: str, target: str, *,
    directed: bool = False,
    disabled: frozenset[str] = frozenset(),
    cost_fn: Callable[[Edge], float] = default_cost,
) -> SearchResult: ...

def neighborhood(
    graph: GraphStore, source: str, k: int, *,
    directed: bool = False,
    disabled: frozenset[str] = frozenset(),
) -> dict[str, int]: ...                              # node_id -> hops from source