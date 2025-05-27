from collections import defaultdict
from typing import TYPE_CHECKING

from advent_of_code.shared.utils import run_solution

if TYPE_CHECKING:
    from collections.abc import Iterable

Lines = list[str]


def create_pc_mapping(lines: Lines) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        left, right = line.split("-")
        mapping[left].add(right)
        mapping[right].add(left)
    return mapping


def is_group(mapping: dict[str, set[str]], possible_group: "Iterable[str]") -> bool:
    for root_pc in possible_group:
        for pc in possible_group:
            if root_pc == pc:
                continue

            if root_pc not in mapping[pc]:
                return False

    return True


def main(lines: Lines) -> None:
    mapping = create_pc_mapping(lines)

    pc_groups: list[set[str]] = []
    for source_pc, linked_pcs in mapping.items():
        if not source_pc.startswith("t"):
            continue

        for linked_pc in linked_pcs:
            for inner_linked_pc in mapping[linked_pc]:
                possible_group = {source_pc, linked_pc, inner_linked_pc}
                if possible_group in pc_groups:
                    continue

                if inner_linked_pc in linked_pcs and is_group(mapping, possible_group):
                    pc_groups.append(possible_group)

    print(len(pc_groups))


if __name__ == "__main__":
    run_solution("2024", "dec_23", main)
