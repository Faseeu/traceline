import itertools
import random

import networkx as nx
import pytest

from traceline.retrieval.graph_search import find_path
from traceline.schemas import Edge, Node
from traceline.storage.graph_store import GraphStore


def build(nodes, edges):
    """edges: list of (id, source, target, confidence)"""
    g = GraphStore()
    for n in nodes:
        g.add_node(Node(id=n, label=n, type="thing"))
    for eid, s, t, c in edges:
        g.add_edge(Edge(id=eid, source=s, target=t, relation="R", confidence=c))
    return g


@pytest.fixture
def viktor():
    return build(
        ["Viktor", "ShellCorp", "BurnerPhone", "Account99"],
        [
            ("e1", "Viktor", "ShellCorp", 0.9),
            ("e2", "ShellCorp", "Account99", 0.8),
            ("e3", "Viktor", "BurnerPhone", 0.7),
            ("e4", "BurnerPhone", "Account99", 0.7),
        ],
    )


def check_consistent(g, result):
    """A found path must be internally consistent."""
    assert len(result.path_edges) == len(result.path_nodes) - 1
    total = sum(1.0 / g.get_edge(e).confidence for e in result.path_edges)
    assert result.total_cost == pytest.approx(total)


# ---------- the Viktor graph ----------


def test_best_path(viktor):
    r = find_path(viktor, "Viktor", "Account99")
    assert r.found and r.reason == "ok"
    assert r.path_nodes == ["Viktor", "ShellCorp", "Account99"]
    assert r.path_edges == ["e1", "e2"]
    assert r.total_cost == pytest.approx(2.361, abs=1e-3)
    assert r.nodes_expanded == 4
    check_consistent(viktor, r)


def test_reroute_when_node_disabled(viktor):
    r = find_path(viktor, "Viktor", "Account99", disabled=frozenset({"ShellCorp"}))
    assert r.path_nodes == ["Viktor", "BurnerPhone", "Account99"]
    assert r.path_edges == ["e3", "e4"]
    assert r.total_cost == pytest.approx(2.857, abs=1e-3)
    assert r.nodes_expanded == 3


def test_no_route_when_both_routes_disabled(viktor):
    r = find_path(
        viktor, "Viktor", "Account99", disabled=frozenset({"ShellCorp", "BurnerPhone"})
    )
    assert not r.found and r.reason == "no_route"


def test_unknown_node(viktor):
    assert find_path(viktor, "Viktor", "Nobody").reason == "unknown_node"
    assert find_path(viktor, "Nobody", "Viktor").reason == "unknown_node"


def test_disabled_endpoints(viktor):
    r = find_path(viktor, "Viktor", "Account99", disabled=frozenset({"Viktor"}))
    assert r.reason == "source_disabled" and not r.found
    r = find_path(viktor, "Viktor", "Account99", disabled=frozenset({"Account99"}))
    assert r.reason == "target_disabled" and not r.found


def test_source_equals_target(viktor):
    r = find_path(viktor, "Viktor", "Viktor")
    assert r.found and r.path_nodes == ["Viktor"] and r.path_edges == []
    assert r.total_cost == 0


# ---------- direction ----------


def test_directed_blocks_reverse_travel(viktor):
    # every edge points away from Viktor, so you can't go back against them
    r = find_path(viktor, "Account99", "Viktor", directed=True)
    assert not r.found and r.reason == "no_route"


def test_undirected_allows_reverse_travel(viktor):
    r = find_path(viktor, "Account99", "Viktor", directed=False)
    assert r.path_nodes == ["Account99", "ShellCorp", "Viktor"]
    assert r.total_cost == pytest.approx(2.361, abs=1e-3)


# ---------- stale entries + custom cost_fn (your course graph) ----------


def test_course_graph_with_custom_cost():
    g = GraphStore()
    for n in "SABG":
        g.add_node(Node(id=n, label=n, type="thing"))
    for eid, s, t, w in [
        ("sa", "S", "A", 1),
        ("sb", "S", "B", 4),
        ("ab", "A", "B", 2),
        ("ag", "A", "G", 8),
        ("bg", "B", "G", 3),
    ]:
        g.add_edge(Edge(id=eid, source=s, target=t, relation="R", properties={"w": w}))
    r = find_path(g, "S", "G", directed=True, cost_fn=lambda e: e.properties["w"])
    assert r.path_nodes == ["S", "A", "B", "G"]
    assert r.path_edges == ["sa", "ab", "bg"]
    assert r.total_cost == 6
    assert r.nodes_expanded == 4  # the stale B(4) entry must NOT be counted


# ---------- parallel edges ----------


def test_parallel_edges_pick_cheaper_one():
    g = build(["A", "B"], [("weak", "A", "B", 0.2), ("strong", "A", "B", 0.9)])
    r = find_path(g, "A", "B")
    assert r.path_edges == ["strong"]


# ---------- trusted reference: networkx ----------


def test_matches_networkx_on_random_graphs():
    for seed in range(30):
        rng = random.Random(seed)
        ids = [f"n{i}" for i in range(12)]
        g = GraphStore()
        for i in ids:
            g.add_node(Node(id=i, label=i, type="thing"))
        undirected, directed_ref = nx.Graph(), nx.DiGraph()
        undirected.add_nodes_from(ids)
        directed_ref.add_nodes_from(ids)

        pairs = [p for p in itertools.combinations(ids, 2) if rng.random() < 0.25]
        for k, (a, b) in enumerate(pairs):
            if rng.random() < 0.5:
                a, b = b, a
            conf = rng.uniform(0.1, 1.0)
            g.add_edge(
                Edge(id=f"e{k}", source=a, target=b, relation="R", confidence=conf)
            )
            undirected.add_edge(a, b, weight=1.0 / conf)
            directed_ref.add_edge(a, b, weight=1.0 / conf)

        for directed, ref in ((False, undirected), (True, directed_ref)):
            result = find_path(g, "n0", "n11", directed=directed)
            try:
                expected = nx.dijkstra_path_length(ref, "n0", "n11", weight="weight")
            except nx.NetworkXNoPath:
                assert not result.found and result.reason == "no_route"
            else:
                assert result.found
                assert result.total_cost == pytest.approx(expected)
                check_consistent(g, result)
