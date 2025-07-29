from dataclasses import dataclass
from enum import Enum, auto
from utils4plans.graphs import Edge, EdgeList
from typing import NamedTuple, TypedDict


# TODO extend edgelist to have a "to-path" feature 

class Path(EdgeList):
    @property
    def path(self):
        # TODO bc/ using NX path library, know the edges will be ordered as a path, but have a simple check for now.. 
        p =  [i.u for i in self.edges] + [self.edges[-1].v]
        assert len(set(p)) == len(self.edges) + 1
        return p
    

class Orientation(Enum):
    X = auto()
    Y = auto()



class GraphPathPair(NamedTuple):
    graph_name: str
    path_ix: int


@dataclass
class STGraph:
    name: str
    paths: list[Path]
    orientation: Orientation

    # TOOD create path dict
    @property
    def path_dict(self):
        return {ix: path for ix, path in enumerate(self.paths)}
    
    @property
    def graph_path_pairs(self):
        return [GraphPathPair(self.name, ix) for ix in range(len(self.paths))]

graph_dict: dict[str, STGraph] = {

}


    # todo be able to return the edges.. which means some named graph dict.. 


@dataclass
class PlanPaths:
    ix: int
    paths: list[GraphPathPair]

    #TODO get the actual edges.. 
    # get the paths. 

# TODO function to assign plan paths uses GraphPathPair and creates a list of planpaths.. 