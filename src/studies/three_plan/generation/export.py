from graph2plan.fourtp.tests import test_degen_cycle
from graph2plan.helpers.utils import get_folder_path
from graph2plan.dual.interfaces import Domains
from graph2plan.rel.rel2 import STGraphs
from rich import print as rprint
from utils4plans.io import read_pickle, write_pickle, write_graph
from studies.quick_paths import LocalStaticPaths
from studies.three_plan.generation.generate import generate_connectivities
from utils4plans.printing import StyledConsole


qp = LocalStaticPaths("three_plan")
DEGEN_PICKLE = "test_degen_cycle_results_250726"


def save_case_and_connectivities(case_name: str, domains: Domains, st_graphs: STGraphs):
    folder_path = get_folder_path(qp.plans, case_name)
    # save floorpan
    domains.write_floorplan(folder_path)
    # save st graphs
    st_graphs.save_rel_graphs(folder_path)
    # save connectivity graphs in a folder..
    # connectivity_folder_path = get_folder_path(folder_path, "connectivity")
    # connectivity_graphs = generate_connectivities(st_graphs)
    # rprint(connectivity_graphs)
    # for ix, graph in enumerate(connectivity_graphs):
    #     write_graph(graph, f"_{ix:02}", connectivity_folder_path)

    StyledConsole.print(f"Finished saving results for {case_name}", style="success")


def run_degen_case_and_write_pickle():
    merged_doms, T1, T2 = test_degen_cycle()
    write_pickle([merged_doms, T1, T2], qp.temp, DEGEN_PICKLE)


if __name__ == "__main__":
    # run_degen_case_and_write_pickle()

    merged_doms, T1, T2 = read_pickle(qp.temp, DEGEN_PICKLE)
    rprint(merged_doms)
    save_case_and_connectivities("three_plan", merged_doms, STGraphs(T1, T2))


## NEXT -> for this case, create folder with plan, T1, T2, and all the graphs..
## maybe for plan2eplus, need to think about what is the core functionality, and then experiments are on top of that.. -> so define a narrow api.. dont try to define the experimenr structure...
