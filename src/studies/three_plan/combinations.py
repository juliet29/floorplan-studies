from rich import print as rprint
from utils4plans.printing import StyledConsole


from itertools import combinations


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