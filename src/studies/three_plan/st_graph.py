from studies.three_plan.interfaces import Orientation, STGraph
from studies.three_plan.paths import path_class
from utils4plans.io import read_graph
from rich import print as rprint
import networkx as nx
from utils4plans.graphs import Edge, EdgeList
from typing import TypeVar

NodeType = TypeVar("NodeType")


def path_to_edgelist(path: list[tuple[NodeType, NodeType]]):
    edges = [Edge(*e) for e in path]
    return EdgeList(edges)


# read a graph..
def get_paths(G: nx.DiGraph, source:NodeType, target:NodeType):
    return [i for i in nx.all_simple_edge_paths(G, source, target)]


if __name__ == "__main__":
    T1 = read_graph("T1", path_class.plans)  # TODO make more consistent signarure
    rprint(T1.nodes)
    # TODO -> to STGRaph..
    source, target = "v_s", "v_n"
    #
    paths = get_paths(nx.DiGraph(T1), source, target)
    rprint(paths)
    pedge = [path_to_edgelist(p) for p in paths] # type: ignore TODO assert each item in path is a tuple.. 

    rprint(pedge)

    T1st = STGraph("T1", paths=pedge, orientation=Orientation.Y)


# /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/studies/static/three_plan/_02_plans/three_plan/T1.json
