from pathlib import Path
from typing import TypeVar

import networkx as nx
from utils4plans.graphs import Edge
from utils4plans.io import read_graph, write_json, read_json
from utils4plans.lists import chain_flatten
from utils4plans.printing import StyledConsole

from studies.three_plan.combinations import create_combinations
from studies.three_plan.export import rprint
from studies.three_plan.interfaces import (
    ConnectivityResult,
    GraphPath,
    GraphPathData,
    Orientation,
    STGraph,
    get_path_from_edges,
    make_graph_paths,
)
from studies.three_plan.paths import (
    CONNECTIVITIES,
    path_class,
    path_to_original_graphs,
    path_to_connectivities,
)

NodeType = TypeVar("NodeType")

ST_NODES = {
    Orientation.Y: ("v_s", "v_n"),
    Orientation.X: ("v_w", "v_e"),
}


def path_to_edgelist(path: list[tuple[NodeType, NodeType]]):
    edges = [Edge(*e) for e in path]
    return GraphPath(edges)


# read a graph..
def get_paths(G: nx.DiGraph, source: NodeType, target: NodeType):
    result = nx.all_simple_edge_paths(G, source, target)
    paths = [i for i in result]
    if len(paths) == 0:
        raise Exception(f"No paths found in G with {G.edges}")

    return paths


def create_stgraph(G: nx.Graph, orientation: Orientation):
    def create_name_based_on_orientation(orientation):
        return f"T{orientation.name}"

    # TODO some check that actually is an st graphs -> can move this check from g2plan to utils
    # TODO move the below into its own function
    source, target = ST_NODES[orientation]
    try:
        assert source in G.nodes
        assert target in G.nodes
    except AssertionError:
        StyledConsole.print(
            f"source or target ({source} | {target}) is missing from graph nodes ({G.nodes})",
            style="error",
        )
        raise Exception  # TODO better error handling?

    paths = get_paths(nx.DiGraph(G), source, target)
    pedge = [path_to_edgelist(p) for p in paths]  # type: ignore TODO assert each item in path is a tuple..
    return STGraph(
        create_name_based_on_orientation(orientation),
        paths=pedge,
        orientation=Orientation.Y,
    )


def create_graph_path_combos(
    local_path=Path(""), G1_name="T1", G2_name="T2"
):  # put default names in object
    T1 = read_graph(
        path_class.plans / local_path, G1_name
    )  # NOTE: this is veryyyy project specific -> assumes this code wont be reused..
    T2 = read_graph(path_class.plans / local_path, G2_name)

    TY = create_stgraph(T1, Orientation.Y)
    TX = create_stgraph(T2, Orientation.X)

    path_pairs = chain_flatten([make_graph_paths(i) for i in [TY, TX]])
    combos = create_combinations(path_pairs)
    return combos, (TY, TX)


def create_jsonable_object(
    combos: list[list[GraphPathData]], st_graphs: tuple[STGraph, STGraph]
):
    graph_paths = {i.name: i.path_dict for i in st_graphs}
    combos_dict = {}
    for ix, combo in enumerate(combos):
        pairs = [i.pair_dict for i in combo]
        combos_dict[ix] = pairs

    json_res = {"graph_paths": graph_paths, "connectivities": combos_dict}
    rprint(json_res)
    return json_res


def create_and_write_graph_path_combos(
    graph_local_path: Path, writing_local_path: Path
):
    combos, st_graphs = create_graph_path_combos(graph_local_path)
    jsonable_object = create_jsonable_object(combos, st_graphs)
    write_json(jsonable_object, path_class.plans / writing_local_path, CONNECTIVITIES, OVERWRITE=True)


def read_graph_combos(local_path=Path("")):
    result: ConnectivityResult = read_json(path_class.plans / local_path, CONNECTIVITIES)
    rprint(result["graph_paths"])
    return result

def get_edges_for_combo(conn_result: ConnectivityResult,num:int):
    # TODO: if need to use independently of these two functions, then consider refactoring..
    graph_paths = conn_result["graph_paths"]
    connectivities = conn_result["connectivities"]
    combo = connectivities[str(num)]
    path_list = [] # TODO renam
    for pair in combo: 
        graph_name = pair["graph"]
        path_ix = pair["path_ix"]
        path = graph_paths[graph_name][str(path_ix)]
        path_list.append(path)

    all_edges = chain_flatten(path_list)
    paths = [get_path_from_edges(i) for i in path_list]

    return all_edges, paths

        # edge = graph_path[pair["graph"]]
    

# TODO: get all edges based on the connectivities.. 


if __name__ == "__main__":
    # TODO have to have some guarantees on this in graph2plan!
    # create_and_write_graph_path_combos(path_to_original_graphs, path_to_connectivities)
    res = read_graph_combos(path_to_connectivities)
    get_edges_for_combo(res, 11)


# /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/studies/static/three_plan/_02_plans/three_plan/T1.json
