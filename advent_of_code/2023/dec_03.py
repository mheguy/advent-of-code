import re
from typing import cast

from advent_of_code.shared.utils import run_solution

Grid = dict[int, str]

DIGITS = "0123456789"
NUM_GAP = re.compile(r"\d\D\d")
NUM = re.compile(r"\d+")
STAR = re.compile(r"\*")
NON_SYMBOLS = re.compile(r"[\.0123456789]")


def safe_get_from_string(index: int, string: str) -> str:
    try:
        return string[index]
    except IndexError:
        return "."


def get_surrounding_chars(match: re.Match[str], row_num: int, grid: dict[int, str]) -> str:
    before_start = match.start() - 1
    after_end = match.end() + 1
    before = safe_get_from_string(before_start, grid[row_num])
    after = safe_get_from_string(match.end(), grid[row_num])
    above = grid[row_num - 1][before_start:after_end]
    below = grid[row_num + 1][before_start:after_end]

    return before + after + above + below


def create_grid(lines: list[str]) -> Grid:
    padding = "." * (len(lines[0]) + 2)
    lines = [f".{line}." for line in lines]
    grid: dict[int, str] = dict(enumerate([padding, *lines, padding]))
    return grid


def get_full_number(grid: Grid, row: int, col: int) -> int:
    # go left
    left_edge = right_edge = col
    while grid[row][left_edge - 1].isdigit():
        left_edge -= 1

    # go right
    right_edge = col
    while grid[row][right_edge + 1].isdigit():
        right_edge += 1

    return int(grid[row][left_edge : right_edge + 1])


def check_horizontal(grid: Grid, row_num: int, col: int) -> list[int]:
    char = grid[row_num][col]
    if char not in DIGITS:
        return []

    return [get_full_number(grid, row_num, col)]


def check_vertical(grid: Grid, row: int, match: re.Match[str]) -> list[int]:
    chars = grid[row][match.start() - 1 : match.end() + 1]

    digits = sum(char.isdigit() for char in chars)
    if digits == 0:
        return []
    if digits == 2:  # noqa: PLR2004
        if re.search(NUM_GAP, chars):
            return [
                get_full_number(grid, row, match.start() - 1),
                get_full_number(grid, row, match.start() + 1),
            ]

        if chars[0].isdigit():
            return [get_full_number(grid, row, match.start())]

        return [get_full_number(grid, row, match.start() + 1)]

    # We have 1 or 3. We need the position of a digit.
    chars_match = cast(re.Match[str], re.search(NUM, chars))
    col = match.start() + chars_match.start() - 1
    return [get_full_number(grid, row, col)]


def get_gear_ratio(match: re.Match[str], row_num: int, grid: dict[int, str]) -> int:
    adjacent_parts: list[int] = []
    adjacent_parts.extend(check_horizontal(grid, row_num, match.start() - 1))
    adjacent_parts.extend(check_horizontal(grid, row_num, match.end()))
    adjacent_parts.extend(check_vertical(grid, row_num - 1, match))
    adjacent_parts.extend(check_vertical(grid, row_num + 1, match))
    if len(adjacent_parts) != 2:  # noqa: PLR2004
        return 0

    return adjacent_parts[0] * adjacent_parts[1]


def main(lines: list[str]) -> None:
    p1_total = 0
    p2_total = 0

    grid = create_grid(lines)

    for row_num, row in grid.items():
        p1_matches = re.finditer(NUM, row)
        for match in p1_matches:
            chars = get_surrounding_chars(match, row_num, grid)
            chars = re.sub(NON_SYMBOLS, "", chars)
            if chars:
                p1_total += int(match[0])

        p2_matches = re.finditer(STAR, row)
        for match in p2_matches:
            p2_total += get_gear_ratio(match, row_num, grid)

    print(p1_total)
    print(p2_total)


if __name__ == "__main__":
    run_solution("2023", "dec_03", main)
