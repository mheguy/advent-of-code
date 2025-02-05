from dataclasses import dataclass
from functools import cached_property

from advent_of_code.shared.utils import run_solution

Lines = list[str]

START_CHAR = "X"
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


@dataclass
class Grid:
    lines: Lines

    @cached_property
    def max_row(self) -> int:
        return len(self.lines) - 1

    @cached_property
    def max_col(self) -> int:
        return len(self.lines[0]) - 1


@dataclass
class Position:
    row: int
    col: int

    def in_grid(self, grid: Grid) -> bool:
        return bool(self.row >= 0 and self.row <= grid.max_row and self.col >= 0 and self.col <= grid.max_col)

    def get_char(self, grid: Grid) -> str:
        return grid.lines[self.row][self.col]


def main(lines: Lines) -> None:
    print(part_1(lines))
    # print(part_2(lines))


def part_1(lines: Lines) -> int:
    results = 0

    grid = Grid(lines)

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == START_CHAR:
                results += search(grid, Position(row, col), char)

    return results


def search(grid: Grid, pos: Position, char: str | None) -> int:
    if char is None:
        return 1

    results = 0

    for row_offset, col_offset in DIRECTIONS:
        current_pos = pos

        for next_char in "MAS":
            current_pos = Position(current_pos.row + row_offset, current_pos.col + col_offset)

            if not current_pos.in_grid(grid):
                break

            if current_pos.get_char(grid) != next_char:
                break
        else:
            results += 1

    return results


def part_2(lines: Lines) -> None:
    print(lines)


if __name__ == "__main__":
    run_solution("2024", "dec_04", main)
