from collections import defaultdict
from typing import TYPE_CHECKING

from advent_of_code.shared.utils import run_solution

if TYPE_CHECKING:
    from collections.abc import Iterable

Lines = list[str]
PcMapping = dict[str, set[str]]


def create_pc_mapping(lines: Lines) -> PcMapping:
    mapping: PcMapping = defaultdict(set)
    for line in lines:
        left, right = line.split("-")
        mapping[left].add(right)
        mapping[right].add(left)
    return mapping


def is_group(mapping: PcMapping, possible_group: "Iterable[str]") -> bool:
    for root_pc in possible_group:
        for pc in possible_group:
            if root_pc == pc:
                continue

            if root_pc not in mapping[pc]:
                return False

    return True


def solve_part_1(mapping: PcMapping) -> None:
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


def get_all_groups_for_pc(mapping: PcMapping, root_pc: str) -> list[set[str]]:
    groups: list[set[str]] = []

    for linked_pc in mapping[root_pc]:
        if any(linked_pc in existing_group for existing_group in groups):
            continue

        current_group = {root_pc}

        for inner_pc in mapping[linked_pc]:
            for group_member in current_group:
                if group_member not in mapping[inner_pc]:
                    break
            else:
                current_group.add(inner_pc)

        current_group.add(linked_pc)

        groups.append(current_group)

    return groups


def get_largest_group_for_pc(mapping: PcMapping, pc: str) -> set[str]:
    groups = get_all_groups_for_pc(mapping, pc)
    return max(*groups, key=lambda x: len(x))


def solve_part_2(mapping: PcMapping) -> None:
    groups: list[set[str]] = []
    for pc in mapping:
        if not pc.startswith("t"):
            continue

        groups.append(get_largest_group_for_pc(mapping, pc))

    largest_group = list(max(*groups, key=lambda x: len(x)))
    largest_group.sort()

    print(",".join(largest_group))


def main(lines: Lines) -> None:
    mapping = create_pc_mapping(lines)

    solve_part_1(mapping)
    solve_part_2(mapping)


if __name__ == "__main__":
    run_solution("2024", "dec_23", main)
