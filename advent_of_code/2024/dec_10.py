from enum import Enum
from typing import cast

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]


MAX_HEIGHT = 9


def main(lines: Lines) -> None:
    grid: dict[Position, int] = {}
    for row, line in enumerate(lines):
        for col, height in enumerate(line):
            grid[Position(col, row)] = int(height)

    summit_count = 0
    trail_count = 0
    for pos, height in grid.items():
        if height != 0:
            continue

        summit_count += len(get_summits_from_trailhead(grid, pos, 0))
        trail_count += len(get_trails_from_trailhead(grid, pos, 0))

    print(summit_count, trail_count)


def get_summits_from_trailhead(grid: dict[Position, int], pos: Position, height: int) -> set[Position]:
    if height == MAX_HEIGHT:
        return {pos}

    summits = set()
    target_height = height + 1

    for direction in Direction:
        next_step = pos + direction.value
        next_height = grid.get(next_step)

        if next_height == target_height:
            summits.update(get_summits_from_trailhead(grid, next_step, cast(int, next_height)))

    return summits


def get_trails_from_trailhead(grid: dict[Position, int], pos: Position, height: int) -> list[Position]:
    if height == MAX_HEIGHT:
        return [pos]

    trails = []
    target_height = height + 1

    for direction in Direction:
        next_step = pos + direction.value
        next_height = grid.get(next_step)

        if next_height == target_height:
            trails.extend(get_trails_from_trailhead(grid, next_step, cast(int, next_height)))

    return trails


if __name__ == "__main__":
    run_solution("2024", "dec_10", main)
