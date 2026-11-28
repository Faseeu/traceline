from collections.abc import Callable

from traceline.schemas import Edge, SearchResult
from traceline.storage.graph_store import GraphStore
import heapq as hp


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
        return SearchResult(found=False,reason= "unknown_node")

    if source in disabled:
        return SearchResult(found=False,reason= "source_disabled")

    if target in disabled:
        return SearchResult(found=False,reason= "target_disabled")

    pass






def neighborhood(
    graph: GraphStore,
    source: str,
    k: int,
    *,
    directed: bool = False,
    disabled: frozenset[str] = frozenset(),
) -> dict[str, int]: ...  # node_id -> hops from source


