import heapq as hq
from collections.abc import Callable
from itertools import count

from traceline.schemas import Edge, SearchResult
from traceline.storage.graph_store import GraphStore


def default_cost(edge: Edge) -> float:  # 1 / confidence
    return 1 / edge.confidence


def find_path(
    graph: GraphStore,
    source: str,
    target: str,
    *,
    directed: bool = False,
    disabled: frozenset[str] = frozenset(),
    cost_fn: Callable[[Edge], float] = default_cost,
) -> SearchResult:
    if not graph.has_node(source) or not graph.has_node(target):
        return SearchResult(found=False, reason="unknown_node")

    if source in disabled:
        return SearchResult(found=False, reason="source_disabled")

    if target in disabled:
        return SearchResult(found=False, reason="target_disabled")
    heap = []
    best = {}
    came_from = {}
    nodes_expanded = 0
    counter = count()

    best[source] = 0
    heap_item = (best[source], next(counter), source)
    hq.heappush(heap, heap_item)
    print(heap, best, came_from)

    while heap:
        cost, _, node = hq.heappop()
        if cost > best[node]:
            continue
        nodes_expanded += 1

        if node == target:
            return SearchResult(
                found=True, total_cost=cost, nodes_expanded=nodes_expanded
            )

        return SearchResult(
            found=False, reason="no_route", nodes_expanded=nodes_expanded
        )

    # TODO: expand neighbours


def neighborhood(
    graph: GraphStore,
    source: str,
    k: int,
    *,
    directed: bool = False,
    disabled: frozenset[str] = frozenset(),
) -> dict[str, int]: ...  # node_id -> hops from source


if __name__ == "__main__":
    from traceline.schemas import Node

    g = GraphStore()
    for n in ["Viktor", "ShellCorp", "BurnerPhone", "Account99"]:
        g.add_node(Node(id=n, label=n, type="thing"))
    g.add_edge(
        Edge(
            id="e1",
            source="Viktor",
            target="ShellCorp",
            relation="OWNS",
            confidence=0.9,
        )
    )
    g.add_edge(
        Edge(
            id="e2",
            source="ShellCorp",
            target="Account99",
            relation="PAID",
            confidence=0.8,
        )
    )
    g.add_edge(
        Edge(
            id="e3",
            source="Viktor",
            target="BurnerPhone",
            relation="USES",
            confidence=0.7,
        )
    )
    g.add_edge(
        Edge(
            id="e4",
            source="BurnerPhone",
            target="Account99",
            relation="CALLED",
            confidence=0.7,
        )
    )

    print(find_path(g, "Viktor", "Account99"))
