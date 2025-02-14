"""Very slow solution since we run the whole patrol route from the start each time.

A better solution would be to add the objects while patrolling so that we only check each branch as needed.
"""

from dataclasses import dataclass
from enum import Enum
from functools import cache

from advent_of_code.shared.utils import run_solution

Lines = list[str]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: "Position|Direction") -> "Position":
        if isinstance(other, Direction):
            other = other.value

        return Position(self.x + other.x, self.y + other.y)


class Direction(Enum):
    UP = Position(0, -1)
    RIGHT = Position(1, 0)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)

    @staticmethod
    def get_next_direction(current_direction: "Direction") -> "Direction":
        return Direction._get_mapping()[current_direction]

    @cache
    @staticmethod
    def _get_mapping() -> "dict[Direction, Direction]":
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }


class Grid:
    def __init__(self, lines: Lines):
        self.row_count = len(lines)
        self.col_count = len(lines[0])
        self.object_grid = [[char == "#" for char in line] for line in lines]

    def __contains__(self, item: Position) -> bool:
        return item.y < self.row_count and item.y >= 0 and item.x < self.col_count and item.x >= 0

    def is_object(self, pos: Position) -> bool:
        try:
            return self.object_grid[pos.y][pos.x]
        except IndexError:
            return False

    def add_object(self, pos: Position) -> None:
        self.object_grid[pos.y][pos.x] = True

    def remove_object(self, pos: Position) -> None:
        self.object_grid[pos.y][pos.x] = False


class Guard:
    def __init__(self, pos: Position):
        self.pos: Position = pos
        self.movement_direction: Direction = Direction.UP
        self.visited_positions: set[Position] = set()

    def patrol(self, grid: Grid) -> bool:
        target_position = self.pos + self.movement_direction

        turns_without_new_positions = 0

        while target_position in grid:
            if turns_without_new_positions >= 4:  # noqa: PLR2004
                return False

            if self.pos in self.visited_positions:
                found_new_position = False
            else:
                self.visited_positions.add(self.pos)
                found_new_position = True

            if grid.is_object(target_position):
                self.movement_direction = Direction.get_next_direction(self.movement_direction)

                if found_new_position:
                    turns_without_new_positions = 0
                else:
                    turns_without_new_positions += 1
            else:
                self.pos = target_position

            target_position = self.pos + self.movement_direction

        return True


def main(lines: Lines) -> None:
    grid = Grid(lines)
    guard_starting_position = get_guard_position(lines)

    guard = Guard(guard_starting_position)
    guard.patrol(grid)
    print(len(guard.visited_positions))

    positions = guard.visited_positions
    positions.remove(guard_starting_position)

    p2_results = 0
    for position in positions:
        grid.add_object(position)

        guard = Guard(guard_starting_position)
        if not guard.patrol(grid):
            p2_results += 1

        grid.remove_object(position)

    print(p2_results)


def get_guard_position(lines: Lines) -> Position:
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "^":
                return Position(col, row)

    raise ValueError("Guard not found")


if __name__ == "__main__":
    run_solution("2024", "dec_06", main)
