from enum import Enum
from typing import cast

from advent_of_code.shared.utils import Position, run_solution

Lines = list[str]


class Direction(Enum):
    UP = Position(0, -1)
    RIGHT = Position(1, 0)
    DOWN = Position(0, 1)
    LEFT = Position(-1, 0)


DIRECTIONS = (Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT)
MAX_HEIGHT = 9


def main(lines: Lines) -> None:
    print(get_result(lines))


def get_result(lines: Lines) -> int | str:
    grid: dict[Position, int] = {}
    for row, line in enumerate(lines):
        for col, height in enumerate(line):
            grid[Position(col, row)] = int(height)

    result = 0
    for pos, height in grid.items():
        if height != 0:
            continue

        summits = get_summits_from_trailhead(grid, pos, 0)
        result += len(summits)

    return result


def get_summits_from_trailhead(grid: dict[Position, int], pos: Position, height: int) -> set[Position]:
    if height == MAX_HEIGHT:
        return {pos}

    summits = set()
    target_height = height + 1

    for direction in DIRECTIONS:
        next_step = pos + direction.value
        next_height = grid.get(next_step)

        if next_height == target_height:
            summits.update(get_summits_from_trailhead(grid, next_step, cast(int, next_height)))

    return summits


if __name__ == "__main__":
    run_solution("2024", "dec_10", main)
