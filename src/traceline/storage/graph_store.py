import networkx as nx

from traceline.schemas import Edge, Node


class GraphStore:
    def __init__(self):
        self._g = nx.MultiDiGraph()
        self._edges: dict[str, Edge] = {}

    def add_node(self, node: Node):

        self._g.add_node(node.id, data=node)

    def add_edge(self, edge: Edge) -> None:  # raises if source/target missin

        if edge.id in self._edges:
            raise ValueError(f"Duplicate _edges can't exist. Edge id: {edge.id}")
        for node_id in (edge.source, edge.target):
            if node_id not in self._g:
                raise ValueError(f"Unknown Node: {node_id}")

        self._g.add_edge(edge.source, edge.target, key=edge.id)
        self._edges[edge.id] = edge

    def get_node(self, node_id: str) -> Node:
        return self._g.nodes[node_id]["data"]

    def get_edge(self, edge_id: str) -> Edge:
        return self._edges[edge_id]

    def has_node(self, node_id):
        return node_id in self._g

    def edges_from(self, node_id: str, *, directed: bool) -> list[tuple[Edge, str]]:
        result = []

        for _, neighbour, key in self._g.out_edges(node_id, keys=True):
            result.append((self._edges[key], neighbour))

        if not directed:
            for _, neighbour, key in self._g.in_edges(node_id, keys=True):
                result.append((self._edges[key], neighbour))

        return result
        # returns (edge, neighbour_id) pairs; if directed=False it also yields incoming _edges
