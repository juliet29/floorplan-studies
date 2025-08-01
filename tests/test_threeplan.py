from math import comb
from studies.three_plan.combinations import create_combinations
from studies.three_plan.st_graph import create_graph_path_combos
from studies.three_plan.paths import path_to_original_graphs



# MORE GENERAL -> combinations stuff

# TODO should this be an assertion or a test?
def calc_expected_len(len_of_lst: int, len_of_longest_combo: int, ):
    combo_lens = [comb(len_of_lst, i) for i in range(len_of_longest_combo+1)]
    return sum(combo_lens)

# TODO parameterize, would be a good place to use hypothesis.. 
def test_len_combinations():
    lst = ["a", "b", "c", "d", "e"]
    all_combos = create_combinations(lst, 4)
    expected_len = calc_expected_len(len(lst), 4)
    assert len(all_combos) == expected_len

def test_content_combinations():
    lst = ["a", "b", "c", "d", "e"]
    all_combos = create_combinations(lst, 4)
    assert ["a", "b","c"] in all_combos 



# THREE PLAN speciifc 
def test_three_plan_combos():
    combos = create_graph_path_combos(local_path=path_to_original_graphs)
    assert len(combos) == 15 # TODO is this safe?
    combo_lens = [len(i) for i in combos]
    assert max(combo_lens) == 4




