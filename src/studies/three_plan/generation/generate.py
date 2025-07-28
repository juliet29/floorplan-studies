import networkx as nx
from graph2plan.helpers.graph_interfaces import (
    CardinalDirectionEnum,
    mapping_for_exterior_vertices,
)
from graph2plan.helpers.utils import chain_flatten
from graph2plan.rel.rel2 import STGraphs
from networkx import relabel_nodes
from rich import print as rprint


from copy import deepcopy
from itertools import combinations


def generate_connectivities(st_graphs: STGraphs):
    # TODO write test for three-cycle graphs => should have four..
    def get_paths(G: nx.DiGraph, source, target):
        return [i for i in nx.all_simple_edge_paths(G, source, target)]

    def create_graph_from_path_combo(path_combo: list[int]):
        G = nx.DiGraph()
        for key in path_combo:
            path = all_paths[key]
            G.add_edges_from(path)

        return G

    T1, T2 = deepcopy(st_graphs)
    relabel_nodes(T1, mapping_for_exterior_vertices(), copy=False)
    relabel_nodes(T2, mapping_for_exterior_vertices(), copy=False)
    # replace name in graph...
    print(T1.edges)
    print(T2.edges)

    T1_source_and_target = (
        CardinalDirectionEnum.SOUTH.name,
        CardinalDirectionEnum.NORTH.name,
    )  # TODO encode in graph /
    T2_source_and_target = (
        CardinalDirectionEnum.WEST.name,
        CardinalDirectionEnum.EAST.name,
    )

    # TODO: map path to graph before chain flatten..
    all_paths = chain_flatten(
        [
            get_paths(G, *nodes)
            for G, nodes in zip([T1, T2], (T1_source_and_target, T2_source_and_target))
        ]
    )
    rprint("all_paths", all_paths)
    all_paths = {(ix + 1): path for ix, path in enumerate(all_paths)}

    all_combinations = []
    for key in all_paths.keys():
        combos = [i for i in combinations(all_paths.keys(), key)]
        all_combinations.extend(combos)

        if key > 4:
            print("Key is > 4.. breaking")
            break

    rprint(f"all combos: {all_combinations}")

    connectivity_graphs = [
        create_graph_from_path_combo(path_combo) for path_combo in all_combinations
    ]
    assert len(connectivity_graphs) == len(all_combinations)

    # map paths and combinations, create graphs

    return connectivity_graphs
