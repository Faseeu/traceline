# src/traceline/storage/graph_store.py
class GraphStore:
    def add_node(self, node: Node) -> None: ...
    def add_edge(self, edge: Edge) -> None: ...      # raises if source/target missing
    def get_node(self, node_id: str) -> Node: ...
    def get_edge(self, edge_id: str) -> Edge: ...
    def edges_from(self, node_id: str, *, directed: bool) -> list[tuple[Edge, str]]: ...
        # returns (edge, neighbour_id) pairs; if directed=False it also yields incoming edges

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