import networkx as nx
from traceline.schemas import Edge, Node


class GraphStore:
    def __init__(self):
        self._g = nx.MultiDiGraph()
        self._edges: dict[str, Edge] = {}

    def add_node(self, node: Node):

        self._g.add_node(node.id, data=node)
    def add_edge(self, edge: Edge) -> None: ...      # raises if source/target missing
    def get_node(self, node_id: str) -> Node: 
        return self._g.nodes[node_id]["data"]
    def get_edge(self, edge_id: str) -> Edge: ...
    def edges_from(self, node_id: str, *, directed: bool) -> list[tuple[Edge, str]]: ...
        # returns (edge, neighbour_id) pairs; if directed=False it also yields incoming edges

