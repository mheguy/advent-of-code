import itertools
import operator

from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    print(part_1(lines))


def part_1(lines: Lines) -> int | str:
    result = 0

    for line in lines:
        result += process_line(line)

    return result


def process_line(line: str) -> int:
    total, others = line.split(": ")
    total = int(total)

    numbers = [int(num) for num in others.split(" ")]

    operators = (operator.add, operator.mul)

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
