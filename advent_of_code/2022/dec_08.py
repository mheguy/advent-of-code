from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from advent_of_code.shared.utils import run_solution

TreeGrid = list[list["Tree"]]


class Side(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


@dataclass
class Tree:
    height: int
    visibility = 0b0000
    views: list[Any] = field(default_factory=list)

    @property
    def score(self) -> int:
        return math.prod(self.views)

    def add_view(self, distance: int) -> None:
        self.views.append(distance)

    def set_side_visible(self, side: Side) -> None:
        self.visibility = self.visibility | (1 << side.value)

    def set_side_invisible(self, side: Side) -> None:
        self.visibility = self.visibility & ~(1 << side.value)

    def is_visible(self, side: Side) -> bool:
        return self.visibility & 1 << side.value != 0


def process_row(row: list[Tree], side: Side) -> None:
    """Set visibility of a row of trees from left-to-right."""
    tallest = 0
    for idx, tree in enumerate(row):
        if idx == 0:
            tallest = tree.height
            tree.set_side_visible(side)
            continue

        if tree.height > tallest:
            tallest = tree.height
            tree.set_side_visible(side)
        else:
            tree.set_side_invisible(side)


def transpose_tree_grid(tree_grid: TreeGrid) -> list[list[Tree]]:
    row = tree_grid[0]
    return [[row[i] for row in tree_grid] for i in range(len(row))]


def process_visibility(tree_grid: TreeGrid) -> None:
    for row in tree_grid:
        process_row(row, Side.WEST)
        process_row(list(reversed(row)), Side.EAST)

    cols = transpose_tree_grid(tree_grid)

    for col in cols:
        process_row(col, Side.NORTH)
        process_row(list(reversed(col)), Side.SOUTH)


def get_list_from_tree_grid(tree_grid: TreeGrid) -> list[Tree]:
    tree_list = []
    for row in tree_grid:
        tree_list.extend(row)
    return tree_list


def process_row_view_distances(row: list[Tree]) -> None:
    """Set view distances of a row of trees looking right to left."""
    for idx, tree in enumerate(row):
        view_distance = 0

        for i in range(idx - 1, -1, -1):
            view_distance += 1
            if tree.height <= row[i].height:
                break

        tree.add_view(view_distance)


def process_view_distances(tree_grid: TreeGrid) -> None:
    for row in tree_grid:
        process_row_view_distances(row)
        process_row_view_distances(list(reversed(row)))

    cols = transpose_tree_grid(tree_grid)

    for col in cols:
        process_row_view_distances(col)
        process_row_view_distances(list(reversed(col)))


def part_1(lines: list[str]) -> None:
    tree_grid = [[Tree(int(char)) for char in line] for line in lines]
    process_visibility(tree_grid)

    tree_list = get_list_from_tree_grid(tree_grid)

    visible_trees = [tree for tree in tree_list if tree.visibility > 0]

    print(f"{len(visible_trees)} trees visible")


def part_2(lines: list[str]) -> None:
    tree_grid = [[Tree(int(char)) for char in line] for line in lines]
    process_view_distances(tree_grid)

    tree_list = get_list_from_tree_grid(tree_grid)

    best_view = max(tree_list, key=lambda x: x.score)

    print(f"{best_view.score} trees visible")


def main(lines: list[str]) -> None:
    part_1(lines)
    part_2(lines)


if __name__ == "__main__":
    run_solution("2022", "dec_08", main)
