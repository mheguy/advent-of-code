from dataclasses import dataclass
from functools import cached_property

from advent_of_code.shared.utils import Position, run_solution

Lines = list[str]

NEXT_CHAR = {"X": "M", "M": "A", "A": "S", "S": None}

DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)

MAS_SET = {"M", "S"}


@dataclass
class Grid:
    lines: Lines

    @cached_property
    def max_row(self) -> int:
        return len(self.lines) - 1

    @cached_property
    def max_col(self) -> int:
        return len(self.lines[0]) - 1

    def get_char(self, pos: Position) -> str | None:
        if not self.in_grid(pos):
            return None

        return self.lines[pos.x][pos.y]

    def in_grid(self, pos: Position) -> bool:
        return bool(pos.x >= 0 and pos.x <= self.max_row and pos.y >= 0 and pos.y <= self.max_col)


def main(lines: Lines) -> None:
    grid = Grid(lines)
    p1_results = 0
    p2_results = 0

    for row, line in enumerate(grid.lines):
        for col, char in enumerate(line):
            if char == "X":
                p1_results += search_for_xmas(grid, Position(row, col))
            if char == "A":
                p2_results += search_for_x_mas(grid, Position(row, col))

    print(p1_results)
    print(p2_results)


def search_for_xmas(grid: Grid, pos: Position) -> int:
    results = 0

    for row_offset, col_offset in DIRECTIONS:
        current_pos = pos

        for next_char in "MAS":
            current_pos = Position(current_pos.x + row_offset, current_pos.y + col_offset)

            if grid.get_char(current_pos) != next_char:
                break
        else:
            results += 1

    return results


def search_for_x_mas(grid: Grid, pos: Position) -> bool:
    n_e = grid.get_char(Position(pos.x - 1, pos.y + 1))
    n_w = grid.get_char(Position(pos.x - 1, pos.y - 1))
    s_e = grid.get_char(Position(pos.x + 1, pos.y + 1))
    s_w = grid.get_char(Position(pos.x + 1, pos.y - 1))

    return bool({(n_e), (s_w)} == MAS_SET and {(n_w), (s_e)} == MAS_SET)


if __name__ == "__main__":
    run_solution("2024", "dec_04", main)
