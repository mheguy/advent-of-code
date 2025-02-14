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
        self._visited_grid = [[False for _ in line] for line in lines]
        self._object_grid = [[char == "#" for char in line] for line in lines]

        self.row_count = len(lines)
        self.col_count = len(lines[0])

    def __contains__(self, item: Position) -> bool:
        return item.y < self.row_count and item.y >= 0 and item.x < self.col_count and item.x >= 0

    def is_object(self, pos: Position) -> bool:
        try:
            return self._object_grid[pos.y][pos.x]
        except IndexError:
            return False


class Guard:
    def __init__(self, pos: Position):
        self.pos: Position = pos
        self.movement_direction: Direction = Direction.UP
        self.visited_positions: set[Position] = set()

    def move(self, grid: Grid) -> None:
        target_position = self.pos + self.movement_direction

        while target_position in grid:
            self.visited_positions.add(self.pos)

            if grid.is_object(target_position):
                self.movement_direction = Direction.get_next_direction(self.movement_direction)
            else:
                self.pos = target_position

            target_position = self.pos + self.movement_direction

        print(f"Exiting at {self.pos} with direction {self.movement_direction}")


def main(lines: Lines) -> None:
    print(part_1(lines))


def part_1(lines: Lines) -> int | str:
    grid = Grid(lines)
    position = get_guard_position(lines)

    guard = Guard(position)

    guard.move(grid)

    return len(guard.visited_positions)


def get_guard_position(lines: Lines) -> Position:
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "^":
                return Position(col, row)

    raise ValueError("Guard not found")


if __name__ == "__main__":
    run_solution("2024", "dec_06", main)
