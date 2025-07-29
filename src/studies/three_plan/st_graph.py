from studies.three_plan.interfaces import Orientation, STGraph, Path
from studies.three_plan.paths import path_class
from utils4plans.io import read_graph
from rich import print as rprint
import networkx as nx
from utils4plans.graphs import Edge
from typing import TypeVar
from utils4plans.printing import StyledConsole
from utils4plans.lists import chain_flatten
from itertools import combinations

NodeType = TypeVar("NodeType")


def path_to_edgelist(path: list[tuple[NodeType, NodeType]]):
    edges = [Edge(*e) for e in path]
    return Path(edges)


# read a graph..
def get_paths(G: nx.DiGraph, source:NodeType, target:NodeType):
    result = nx.all_simple_edge_paths(G, source, target)
    paths =  [i for i in result]
    if len(paths) == 0:
        raise Exception(f"No paths found in G with {G.edges}")

    return paths

st_nodes = {
    Orientation.Y : ("v_s", "v_n"),
    Orientation.X : ("v_w", "v_e"),

    }

def create_stgraph(graph_name:str, orientation: Orientation):
    def create_name_based_on_orientation(orientation):
        return f"T{orientation.name}"
    G = read_graph(graph_name, path_class.plans)

    # TODO some check that actually is an st graphs -> can move this check from g2plan to utils 
    # TODO move the below into its own function 
    source, target = st_nodes[orientation]
    try:
        assert source in G.nodes
        assert target in G.nodes
    except AssertionError:
        StyledConsole.print(f"source or target ({source} | {target}) is missing from graph nodes ({G.nodes})", style="error")
        raise Exception # TODO better error handling? 
    
    paths = get_paths(nx.DiGraph(G), source, target)
    pedge = [path_to_edgelist(p) for p in paths] # type: ignore TODO assert each item in path is a tuple.. 
    return STGraph(create_name_based_on_orientation(orientation), paths=pedge, orientation=Orientation.Y)



# TODO move to. own page 
def create_combinations(items: list, len_of_max_combo: int | None = None):
    if not len_of_max_combo:
        len_of_max_combo = len(items)
    else:
        assert len_of_max_combo <= len(items)
    enumerated_items = {(ix + 1): path for ix, path in enumerate(items)}
    
    all_combinations = []
    for key in enumerated_items.keys():
        combos = [i for i in combinations(enumerated_items.keys(), key)]
        all_combinations.extend(combos)


    
        if key > len_of_max_combo:
            StyledConsole.print(f"Key is > {len_of_max_combo}.. breaking", style="info")
            break
    
    rprint(f"all combos: {all_combinations}")
    res = []
    for combo in all_combinations:
        dres = [enumerated_items[i] for i in combo]
        res.append(dres)

    return res





def assign_paths_to_plans(graph_dict: dict[str, STGraph]):
    TX = graph_dict["TX"]
    TY = graph_dict["TY"]

    # all combinations of paths.. 
    path_pairs = chain_flatten([TX.graph_path_pairs, TY.graph_path_pairs])
    combos = create_combinations(path_pairs)
    return path_pairs







if __name__ == "__main__":
    # TODO have to have some guarantees on this in graph2plan! 
    TY = create_stgraph("T1", Orientation.Y) 
    TX = create_stgraph("T2", Orientation.X) 
    gd = {
        TX.name: TX,
        TY.name: TY
    }
    assign_paths_to_plans(gd)
    print("end")



# /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/studies/static/three_plan/_02_plans/three_plan/T1.json
