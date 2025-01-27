from enum import IntEnum
from itertools import pairwise

from advent_of_code.shared.utils import run_solution

Level = str
LOWER_LIMIT = 1
UPPER_LIMIT = 3


class Direction(IntEnum):
    DECREASING = 0
    INCREASING = 1
    UNKNOWN = 2


def main(reports: list[Level]) -> None:
    safe_reports = 0
    for report in reports:
        levels = [int(level) for level in report.split()]

        direction: Direction = Direction.UNKNOWN

        for left, right in pairwise(levels):
            difference = left - right
            if abs(difference) < LOWER_LIMIT or abs(difference) > UPPER_LIMIT:
                # Unsafe
                break

            current_direction = Direction(difference < 0)

            if direction is Direction.UNKNOWN:
                direction = current_direction

            if direction != current_direction:
                # Unsafe
                break

        else:
            # Safe
            safe_reports += 1

    print(safe_reports)


if __name__ == "__main__":
    run_solution("2024", "dec_02", main)
