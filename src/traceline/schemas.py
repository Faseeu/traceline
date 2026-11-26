from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field


class Evidence(BaseModel):
    """One piece of proof for an edge: where it came from and what it said."""
    model_config = ConfigDict(frozen=True)
    chunk_id: str
    quote: str = ""


class Node(BaseModel):
    id: str
    label: str
    type: str                      # free string, not an enum
    properties: dict[str, Any] = Field(default_factory=dict)
    chunk_ids: list[str] = Field(default_factory=list)


class Edge(BaseModel):
    id: str
    source: str
    target: str
    relation: str                  # free string
    confidence: float = Field(default=1.0, gt=0.0, le=1.0)   # gt=0: cost is 1/confidence
    evidence: list[Evidence] = Field(default_factory=list)
    properties: dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    found: bool
    path_nodes: list[str] = Field(default_factory=list)
    path_edges: list[str] = Field(default_factory=list)      # edge ids, in order
    total_cost: float = 0.0
    nodes_expanded: int = 0
    reason: Literal["ok", "no_route", "source_disabled", "target_disabled", "unknown_node"] = "ok"