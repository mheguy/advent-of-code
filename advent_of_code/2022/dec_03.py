import itertools
import string
from typing import Any

from advent_of_code.shared.utils import run_solution


def get_priority_map() -> dict[str, int]:
    return {
        char: index
        for index, char in enumerate(itertools.chain(string.ascii_lowercase, string.ascii_uppercase), start=1)
    }


def create_groups_of_n(list_to_split: list[str], group_size: int) -> list[list[str]]:
    num_groups = len(list_to_split) // group_size

    index = 0
    groups = []
    for _ in range(num_groups):
        groups.append(list_to_split[index : index + 3])
        index += group_size

    return groups


def find_badge(group: list[str]) -> str:
    possible_badges: dict[int, set[Any]] = {
        member_number: {item for item in member_backpack if item in group[-1]}
        for member_number, member_backpack in enumerate(group[:-1])
    }

    if badge := next(
        (bag_item for bag_item in possible_badges[0] if bag_item in possible_badges[1]),
        None,
    ):
        return badge
    raise ValueError


def main(lines: list[str]) -> None:
    priority_map = get_priority_map()

    total = 0
    for line in lines:
        midpoint = len(line) // 2
        left = line[:midpoint]
        right = line[midpoint:]
        for char in left:
            if char in right:
                total += priority_map[char]
                break

    print(total)

    groups_of_3 = create_groups_of_n(lines, 3)

    total = 0
    for group in groups_of_3:
        badge = find_badge(group)
        total += priority_map[badge]

    print(total)


if __name__ == "__main__":
    run_solution("2022", "dec_03", main)
