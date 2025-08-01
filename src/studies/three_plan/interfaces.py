from dataclasses import dataclass
from enum import Enum, auto
from typing_extensions import Literal
from altair import Type
from utils4plans.graphs import Edge, EdgeList
from typing import NamedTuple, TypedDict


# TODO extend edgelist to have a "to-path" feature
#
#


class GraphPath(EdgeList):
    @property
    def path(self):  # TODO -> dont need this anymore
        # TODO bc/ using NX path library, know the edges will be ordered as a path, but have a simple check for now..
        p = [i.u for i in self.edges] + [self.edges[-1].v]
        assert len(set(p)) == len(self.edges) + 1
        return p
        # maybe this is better as a function..

    @property
    def to_json(self):
        return [i.pair for i in self.edges]


class Orientation(Enum):
    X = auto()
    Y = auto()

    # maybe best thing here is to pass the graph, and then it has the pair as an attribute..


@dataclass
class STGraph:
    name: str
    paths: list[GraphPath]
    orientation: Orientation

    # TOOD create path dict
    @property
    def path_dict(self):
        return {ix: path.to_json for ix, path in enumerate(self.paths)}


class GraphPathData(NamedTuple):
    G: STGraph
    path_ix: int

    @property
    def pair(self):
        return (self.G.name, self.path_ix)

    @property
    def pair_dict(self):
        return {"graph": self.G.name, "path_ix": self.path_ix}

    @property
    def path(self):
        return self.G.paths[self.path_ix]


def make_graph_paths(G: STGraph):
    return [GraphPathData(G, ix) for ix in range(len(G.paths))]

    # todo be able to return the edges.. which means some named graph dict..


EdgeType = tuple[str, str]


def get_path_from_edges(_edges: list[EdgeType]):
    # TODO bc/ using NX path library, know the edges will be ordered as a path, but have a simple check for now..
    # TODO: IS THIS SOMETHING networkx can do?
    edges = [Edge(*i) for i in _edges]
    p = [i.u for i in edges] + [edges[-1].v]
    assert len(set(p)) == len(edges) + 1
    return p


class GraphPathsDict(TypedDict):
    TY: dict[str, list[tuple[str, str]]]
    TX: dict[str, list[tuple[str, str]]]


class ConnectivitiesDictInner(TypedDict):
    graph: Literal["TX", "TY"]
    path_ix: int


class ConnectivityResult(TypedDict):
    graph_paths: GraphPathsDict
    connectivities: dict[str, list[ConnectivitiesDictInner]]


# @dataclass
# class PlanPaths:
#     ix: int
#     paths: list[GraphPath]

#     #TODO get the actual edges..
#     # get the paths.

# # TODO function to assign plan paths uses GraphPathPair and creates a list of planpaths..
