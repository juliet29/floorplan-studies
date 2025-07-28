from dataclasses import dataclass
from enum import Enum, auto
from utils4plans.graphs import Edge, EdgeList
from typing import NamedTuple


class Orientation(Enum):
    X = auto()
    Y = auto()


@dataclass
class STGraph:
    name: str
    paths: list[EdgeList]
    orientation: Orientation

    # TODO create from networkx graph, orientation (use to get source/target nodes.. )

    # TOOD create path dict
    def create_path_dict(self):
        return {ix: path for ix, path in enumerate(self.paths)}


class GraphPathPair(NamedTuple):
    graph: str
    path_ix: int

# TODO function to assign plan paths uses GraphPathPair 

@dataclass
class PlanPaths:
    ix: int
    paths: list[GraphPathPair]

    #TODO get the actual edges.. 
    # get the paths. 
