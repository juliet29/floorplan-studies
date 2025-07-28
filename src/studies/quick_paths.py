from dataclasses import dataclass
from enum import StrEnum
from studies.base_paths import BASE_PATH
from rich import print as rprint
from utils4plans.printing import StyledConsole
from utils4plans.paths import StaticPaths

from typing import Literal
from pathlib import Path


# TODO this will maybe be common amongst all the studies.. hence a package or separate package ~ studyhelpers









ProjectNames = Literal["three_plan", "graph_bem", "p1_1_gen"]


@dataclass(frozen=True)
class LocalStaticPaths(StaticPaths):
    name: ProjectNames
    base_path: Path = BASE_PATH


if __name__ == "__main__":
    pass
    q = LocalStaticPaths("three_plan")
    rprint(q.temp)
    # CustomConsole.print("hello", style="info")
    # CustomConsole.print("hello", style="success")
    # CustomConsole.print("hello", style="warning")
