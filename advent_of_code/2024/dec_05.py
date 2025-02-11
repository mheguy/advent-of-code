from collections import defaultdict

from advent_of_code.shared.utils import run_solution

Lines = list[str]


def main(lines: Lines) -> None:
    rules: dict[int, list[int]] = defaultdict(list)

    slice_loc = 0
    for idx, line in enumerate(lines):
        if not line:
            slice_loc = idx
            break

        earlier, later = map(int, line.split("|"))
        rules[later].append(earlier)

    updates = [list(map(int, line.split(","))) for line in lines[slice_loc + 1 :] if line]

    good_update_result = 0
    bad_update_result = 0

    for update in updates:
        if is_valid_udpate(rules, update):
            good_update_result += update[len(update) // 2]
        else:
            bad_update_result += get_bad_update_value(rules, update)

    print(good_update_result)
    print(bad_update_result)


def is_valid_udpate(rules: dict[int, list[int]], update: list[int]) -> bool:
    for idx, num in enumerate(update):
        for earlier_num in rules[num]:
            if earlier_num in update[idx:]:
                return False

    return True


def get_bad_update_value(rules: dict[int, list[int]], update: list[int]) -> int:
    return 0


if __name__ == "__main__":
    run_solution("2024", "dec_05", main)
