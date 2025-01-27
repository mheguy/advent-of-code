import re
from itertools import groupby

from advent_of_code.shared.utils import run_solution

CrateStack = list[str]


def initialize_columns(setup_lines: list[str]) -> dict[str, CrateStack]:
    clean_setup_lines = [line[1::4] for line in setup_lines]
    col_headers = clean_setup_lines[-1]
    clean_setup_lines = reversed(clean_setup_lines[:-1])
    columns = {x: [] for x in col_headers}
    for line in clean_setup_lines:
        for col_num, char in enumerate(line, start=1):
            if char != " ":
                columns[str(col_num)].append(char)
    return columns


def process_instruction_line(columns: dict[str, CrateStack], line: str) -> None:
    if not line:
        return

    result = re.search(r"\w+ (\d+) \w+ (\d+) \w+ (\d+)", line)
    if not result:
        raise ValueError(f"Invalid instruction: {line}")

    qty_to_move, origin, destination = result.groups()
    for _ in range(int(qty_to_move)):
        columns[destination].append(columns[origin].pop())


def part_1(lines: list[str]) -> None:
    setup, instructions = (list(group) for key, group in groupby(lines, bool) if key)

    columns = initialize_columns(setup)
    for line in instructions:
        process_instruction_line(columns, line)

    top_crates = [stack.pop() for stack in columns.values()]
    print("".join(top_crates))


def process_instruction_line_part_2(columns: dict[str, CrateStack], line: str) -> None:
    if not line:
        return

    result = re.search(r"\w+ (\d+) \w+ (\d+) \w+ (\d+)", line)
    if not result:
        raise ValueError(f"Invalid instruction: {line}")

    qty_to_move_str, origin, destination = result.groups()
    qty_to_move = int(qty_to_move_str)

    taken_crates = [columns[origin].pop() for _ in range(qty_to_move)]
    taken_crates.reverse()

    for n in range(qty_to_move):
        columns[destination].append(taken_crates[n])


def part_2(lines: list[str]) -> None:
    setup, instructions = (list(group) for key, group in groupby(lines, bool) if key)

    columns = initialize_columns(setup)
    for line in instructions:
        process_instruction_line_part_2(columns, line)

    top_crates = [stack.pop() for stack in columns.values()]
    print("".join(top_crates))


def main(lines: list[str]) -> None:
    part_1(lines)
    part_2(lines)


if __name__ == "__main__":
    run_solution("2022", "dec_05", main)
