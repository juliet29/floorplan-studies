from math import comb
from studies.three_plan.st_graph import create_combinations

# TODO should this be an assertion or a test?
def calc_expected_len(len_of_lst: int, len_of_longest_combo: int, ):
    combo_lens = [comb(len_of_lst, i) for i in range(len_of_longest_combo+1)]
    return sum(combo_lens)

# TODO parameterize 


def test_len_combinations():
    lst = ["a", "b", "c", "d", "e"]
    all_combos = create_combinations(lst, 4)
    expected_len = calc_expected_len(len(lst), 4)
    assert len(all_combos) == expected_len

def test_content_combinations():
    lst = ["a", "b", "c", "d", "e"]
    all_combos = create_combinations(lst, 4)
    assert ["a", "b","c"] in all_combos 

