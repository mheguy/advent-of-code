import itertools
import operator
from typing import TYPE_CHECKING

from advent_of_code.shared.utils import run_solution

if TYPE_CHECKING:
    from collections.abc import Callable

Lines = list[str]


def main(lines: Lines) -> None:
    print(get_result(lines, (operator.add, operator.mul)))
    print(get_result(lines, (operator.add, operator.mul, concat_numbers)))


def concat_numbers(left: int, right: int) -> int:
    return int(f"{left}{right}")


def get_result(lines: Lines, operators: tuple["Callable[[int, int], int]", ...]) -> int:
    result = 0

    for line in lines:
        result += process_line(line, operators)

    return result


def process_line(line: str, operators: tuple["Callable[[int, int], int]", ...]) -> int:
    total, others = line.split(": ")
    total = int(total)

    numbers = [int(num) for num in others.split(" ")]

    operator_combinations = list(itertools.product(operators, repeat=len(numbers) - 1))

    for operator_combination in operator_combinations:
        running_total = numbers[0]

        for num, op in zip(numbers[1:], operator_combination, strict=True):
            running_total = op(running_total, num)

        if total == running_total:
            return total

    return 0


if __name__ == "__main__":
    run_solution("2024", "dec_07", main)
