import itertools
from typing import TYPE_CHECKING

from advent_of_code.shared.utils import run_solution

if TYPE_CHECKING:
    from collections.abc import Iterable

Lines = list[str]


def main(lines: Lines) -> None:
    p1_result = 0

    cost_mappings: list[dict[tuple[int, ...], int]] = []
    for line in lines:
        if not line:
            continue

        banana_costs = [0, 0, 0]

        num = int(line)

        for _ in range(2000):
            num = run_secret_num_sequence(num)
            banana_costs.append(int(str(num)[-1:]))

        p1_result += num

        delta_list = []
        for left, right in nwise(banana_costs, 2):
            delta_list.append(left - right)

        cost_mapping: dict[tuple[int, ...], int] = {}

        for delta_set, banana_cost in zip(nwise(delta_list, 4), banana_costs[4:], strict=True):
            if delta_set in cost_mapping:
                continue

            cost_mapping[delta_set] = banana_cost

        cost_mappings.append(cost_mapping)

    valid_numbers = tuple(range(-9, 9 + 1, 1))
    valid_combinations = list(itertools.product(valid_numbers, repeat=4))

    max_bananas = 0  # "Max Bananas" was also my nickname in high school

    for valid_combination in valid_combinations:
        total_bananas = 0
        for cost_mapping in cost_mappings:
            total_bananas += cost_mapping.get(valid_combination, 0)

        max_bananas = max(max_bananas, total_bananas)

    print(p1_result)
    print(max_bananas)


def nwise(iterable: list[int], n: int) -> "Iterable[tuple[int, ...]]":
    iterators = itertools.tee(iterable, n)
    for i, it in enumerate(iterators):
        for _ in range(i):
            next(it, None)
    return zip(*iterators, strict=False)


def run_secret_num_sequence(num: int) -> int:
    tmp_num = num * 64
    tmp_num = tmp_num ^ num
    num = tmp_num % 16777216

    tmp_num = num // 32
    tmp_num = tmp_num ^ num
    num = tmp_num % 16777216

    tmp_num = num * 2048
    tmp_num = tmp_num ^ num
    return tmp_num % 16777216


if __name__ == "__main__":
    run_solution("2024", "dec_22", main)
